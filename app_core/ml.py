"""Classificação real de sentimento: TF-IDF + regressão logística."""
import csv
import json
from functools import lru_cache
from pathlib import Path
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from .config import ROOT, model_path

LABELS = ('negativo','neutro','positivo')

def load_dataset():
    with (ROOT/'data'/'sentiment_train.csv').open(encoding='utf-8',newline='') as f:
        rows=list(csv.DictReader(f))
    if len(rows)<30 or not set(LABELS).issubset({r['label'] for r in rows}):
        raise ValueError('Dataset insuficiente ou rótulos incompletos')
    return [r['text'] for r in rows],[r['label'] for r in rows],[r['template_group'] for r in rows]

def train(save=True):
    texts, labels, groups = load_dataset()
    # Impede que quatro variações do mesmo texto-base caiam em treino e teste.
    splitter=StratifiedGroupKFold(n_splits=4,shuffle=True,random_state=42)
    it, iv = next(splitter.split(texts,labels,groups))
    xt=[texts[i] for i in it]; xv=[texts[i] for i in iv]
    yt=[labels[i] for i in it]; yv=[labels[i] for i in iv]
    pipe=Pipeline([
       ('tfidf',TfidfVectorizer(strip_accents='unicode',lowercase=True,ngram_range=(1,2),min_df=1,sublinear_tf=True)),
       ('model',LogisticRegression(max_iter=1500,class_weight='balanced',random_state=42))
    ])
    pipe.fit(xt,yt)
    pred=pipe.predict(xv)
    report={'evaluation':'StratifiedGroupKFold / held-out template groups',
            'training_samples':len(xt),'test_samples':len(xv),
            'accuracy':round(float(accuracy_score(yv,pred)),4),
            'labels':list(LABELS),
            'confusion_matrix':confusion_matrix(yv,pred,labels=LABELS).tolist(),
            'per_class':classification_report(yv,pred,labels=LABELS,output_dict=True,zero_division=0)}
    if save:
        dest=model_path(); dest.parent.mkdir(parents=True,exist_ok=True)
        joblib.dump(pipe,dest)
        (dest.parent/'metrics.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
        get_model.cache_clear()
    return report

@lru_cache(maxsize=1)
def get_model():
    dest=model_path()
    if not dest.exists():
        train(save=True)
    return joblib.load(dest)

def predict(text):
    model=get_model()
    probabilities=model.predict_proba([text])[0]
    labels=model.classes_
    probs={str(label):round(float(prob),4) for label,prob in zip(labels,probabilities)}
    best=max(probs,key=probs.get)
    return {'label':best,'confidence':probs[best],'probabilities':probs,
            'note':'Modelo experimental treinado em dados sintéticos; probabilidades não são certezas.'}

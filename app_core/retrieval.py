"""Busca vetorial TF-IDF sobre fontes locais rastreáveis (não é embedding neural)."""
import re
import unicodedata
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .db import docs_for_retrieval

STOP_PT = {
 'a','o','os','as','um','uma','de','do','da','dos','das','em','no','na','nos','nas',
 'para','por','com','sem','que','qual','quais','como','quanto','quantos','quanta','tem',
 'ter','me','eu','voce','voces','e','ou','é','sao','ser','se','pode','posso','sobre','ha',
 'existe','existem','quero','gostaria','favor','onde','aqui','cardapio','restaurante','produto'
}
def tokens(text):
    plain=unicodedata.normalize('NFKD',text.lower()).encode('ascii','ignore').decode('ascii')
    return set(t for t in re.findall(r'[a-z0-9]+',plain) if len(t)>2 and t not in STOP_PT)

def retrieve(question, top_k=3, min_similarity=0.13):
    docs=docs_for_retrieval()
    if not docs or not tokens(question): return []
    corpus=[d['title']+' '+d['content'] for d in docs]
    vec=TfidfVectorizer(strip_accents='unicode',lowercase=True,ngram_range=(1,2),
                        stop_words=sorted(STOP_PT),sublinear_tf=True)
    matrix=vec.fit_transform(corpus)
    q=vec.transform([question]); scores=cosine_similarity(q,matrix)[0]
    q_terms=tokens(question)
    ranking=sorted(enumerate(scores),key=lambda t:t[1],reverse=True)
    matches=[]
    for i,score in ranking:
        doc=docs[i]
        overlap=q_terms & tokens(doc['title']+' '+doc['content'])
        if score<min_similarity or not overlap: continue
        matches.append({'id':doc['id'],'title':doc['title'],'kind':doc['kind'],
                        'content':doc['content'],'score':round(float(score),4)})
        if len(matches)>=top_k:break
    return matches

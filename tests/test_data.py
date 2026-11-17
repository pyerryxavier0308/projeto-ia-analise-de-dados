from app_core.db import seed, connection, products
from app_core.ml import train, predict

def test_seed_idempotent(client):
    a=seed();b=seed()
    assert a==b

def test_sql_injection_filter_is_parameterized(client):
    # Entradas hostis são tratadas como valores, nunca como comandos SQL.
    assert products(category="Pizza' OR 1=1 --")==[]
    assert len(products())>=10

def test_ml_training_metrics(client):
    report=train(save=False)
    assert report['training_samples']>200
    assert 0<=report['accuracy']<=1
    assert len(report['confusion_matrix'])==3

def test_review_is_saved(client):
    with connection() as db:
        r=db.execute('SELECT COUNT(*) FROM reviews').fetchone()[0]
        assert r>0

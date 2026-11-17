def test_health(client):
    out=client.get('/api/health')
    assert out.status_code==200
    assert out.json()['status']=='ok'

def test_menu_and_analytics(client):
    r=client.get('/api/menu').json()['items']
    assert len(r)>=10
    assert all('price' in x for x in r)
    s=client.get('/api/analytics').json()
    assert s['total_reviews']>=50
    assert sum(s['sentiment_counts'].values())==s['total_reviews']

def test_sentiment(client):
    r=client.post('/api/sentiment',json={'text':'A comida estava excelente, deliciosa e chegou quentinha'})
    assert r.status_code==200
    assert r.json()['label'] in {'positivo','negativo','neutro'}
    assert abs(sum(r.json()['probabilities'].values())-1)<0.001

def test_add_review_updates_analytics(client):
    before=client.get('/api/analytics').json()['total_reviews']
    r=client.post('/api/reviews',json={'product_id':1,'rating':5,'text':'Comida maravilhosa e muito saborosa'})
    assert r.status_code==201
    assert r.json()['review']['product_id']==1
    assert client.get('/api/analytics').json()['total_reviews']==before+1

def test_invalid_requests(client):
    assert client.post('/api/reviews',json={'product_id':9999,'rating':5,'text':'Experiência agradável'}).status_code==404
    assert client.post('/api/reviews',json={'product_id':1,'rating':9,'text':'Experiência agradável'}).status_code==422
    assert client.post('/api/sentiment',json={'text':'a'}).status_code==422
    assert client.get('/api/reviews?limit=9000').status_code==422

def test_recommend_filters(client):
    result=client.post('/api/recommend',json={'vegan':True,'avoid_lactose':True,'max_price':50}).json()
    assert result['items']
    assert all(p['vegan'] and not p['contains_lactose'] and p['price']<=50 for p in result['items'])

def test_assistant_has_sources(client):
    res=client.post('/api/ask',json={'question':'Qual é o horário de funcionamento?'}).json()
    assert res['grounded'] is True
    assert res['sources']
    assert res['mode']=='offline'

def test_assistant_unknown_falls_back(client):
    res=client.post('/api/ask',json={'question':'Qual é a capital da França?'}).json()
    assert res['grounded'] is False
    assert res['sources']==[]


def test_vegan_structured_query(client):
    res=client.post('/api/ask',json={'question':'Quais opções veganas tem?'}).json()
    assert res['grounded'] is True
    assert res['mode']=='structured'
    assert 'Pizza Vegana' in res['answer']
    assert all(s['id'].startswith('menu:') for s in res['sources'])


def test_structured_sources_not_fictional_similarity(client):
    res = client.post('/api/ask', json={'question': 'Quais são as opções veganas?'}).json()
    assert res['mode'] == 'structured'
    assert all(s['score'] is None for s in res['sources'])
    assert '- **Pizza Vegana**' in res['answer']
    assert 'R$ 49,00' in res['answer']

def test_personal_order_has_no_sources(client):
    res = client.post('/api/ask', json={'question': 'Qual o nome do entregador do meu último pedido?'}).json()
    assert res['grounded'] is False
    assert res['sources'] == []
    assert 'não tenho acesso' in res['answer'].lower()

def test_recommender_explains_filters(client):
    out = client.post('/api/recommend',json={
        'vegan':True,'avoid_lactose':True,'max_price':35,'spicy':False
    }).json()
    assert out['items']
    for item in out['items']:
        reason = item['why_recommended'].lower()
        assert 'vegano' in reason and 'lactose' in reason and 'r$ 35,00' in reason
        assert item['vegan'] and not item['contains_lactose'] and not item['spicy']

def test_brazilian_money_format():
    from app_core.formatters import format_brl
    assert format_brl(31.5)=='R$ 31,50'
    assert format_brl(1234.5)=='R$ 1.234,50'

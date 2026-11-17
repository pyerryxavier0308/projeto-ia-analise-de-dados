"""Dashboard Streamlit para o Projeto de IA — Análise de Dados.

Execute com: python -m streamlit run dashboard/app.py
A API precisa estar ativa em http://127.0.0.1:8000.
"""
import os
import requests
import pandas as pd
import streamlit as st

st.set_page_config(page_title='Projeto de IA — Análise de Dados',page_icon='🍽️',layout='wide',initial_sidebar_state='expanded')
API=os.environ.get('PROJECT_API_URL','http://127.0.0.1:8000').rstrip('/')
TIMEOUT=20

def fmt_brl(amount):
    """Formata valores em reais no padrão brasileiro."""
    value=f'{float(amount):,.2f}'
    return 'R$ '+value.replace(',', 'TEMP').replace('.', ',').replace('TEMP', '.')

st.markdown('''<style>
.block-container {padding-top: 1.7rem; max-width: 1300px;}
[data-testid="stMetric"] {background: rgba(97, 136, 128, 0.09);border: 1px solid rgba(130, 160, 160, 0.25);border-radius: 12px;padding: 14px;}
h1,h2,h3 {letter-spacing:-0.02em;}
.small-note {color:#88979a;font-size:0.84rem;}
</style>''',unsafe_allow_html=True)

@st.cache_data(ttl=4)
def api_get(endpoint):
    r=requests.get(f'{API}{endpoint}',timeout=TIMEOUT)
    r.raise_for_status();return r.json()

def api_post(endpoint, payload):
    r=requests.post(f'{API}{endpoint}',json=payload,timeout=TIMEOUT)
    if not r.ok:
        try: d=r.json().get('detail',r.text)
        except ValueError: d=r.text
        raise RuntimeError(f'Erro {r.status_code}: {d}')
    st.cache_data.clear();return r.json()

with st.sidebar:
    st.title('🍽️ Projeto de IA')
    st.caption('Laboratório de IA e dados')
    st.divider()
    try:
        health=api_get('/api/health')
        st.success('API conectada', icon='✅')
    except requests.RequestException:
        st.error('API indisponível',icon='⚠️')
        st.code('python -m uvicorn app_core.api:app --reload',language='powershell')
        st.info('Abra um terminal separado e inicie a API antes de usar o dashboard.')
        st.stop()
    st.caption(f'API: {API}')
    st.divider()
    st.info('Todos os restaurantes, produtos, preços e avaliações são fictícios. Esta aplicação é uma demonstração educacional; não recebe pedidos nem pagamentos reais.')
    llm_flag=st.toggle('Usar LLM externo (opcional)',value=False,
                       help='Exige OPENAI_API_KEY configurada no ambiente do processo da API. Pode gerar cobrança.')

st.title('Inteligência de dados para restaurantes')
st.caption('Análise de avaliações • Busca fundamentada • Recomendações explicáveis • API REST')

tabs=st.tabs(['📊 Visão geral','🧠 Análise de sentimento','💬 Assistente','🍔 Cardápio e recomendações','🗃️ Avaliações'])

with tabs[0]:
    stats=api_get('/api/analytics')
    items=api_get('/api/menu')['items']
    a,b,c,d=st.columns(4)
    a.metric('Avaliações',stats['total_reviews'])
    b.metric('Nota média',f"{stats['average_rating']:.2f} / 5")
    c.metric('Produtos',len(items))
    d.metric('Avaliações positivas',stats['sentiment_counts']['positivo'])
    st.subheader('Distribuição de sentimentos')
    chart=pd.DataFrame([{'Sentimento':x.title(),'Quantidade':n} for x,n in stats['sentiment_counts'].items()])
    st.bar_chart(chart.set_index('Sentimento'),height=270)
    st.subheader('Produtos avaliados')
    prods=pd.DataFrame(stats['by_product'])
    if not prods.empty:
        prods.columns=['Produto','Avaliações','Nota média']
        st.dataframe(prods,hide_index=True,use_container_width=True)
    st.caption('Os rótulos das avaliações iniciais foram criados artificialmente. Novas avaliações usam a previsão do modelo.')

with tabs[1]:
    st.subheader('Classificador treinado com Machine Learning')
    st.markdown('TF-IDF + regressão logística. O modelo **aprende padrões de exemplos**, não é um LLM.')
    sample=st.text_area('Escreva uma avaliação',value='A pizza estava deliciosa e chegou quentinha!',height=110,max_chars=1000)
    if st.button('Classificar avaliação',type='primary'):
        try:
            r=api_post('/api/sentiment',{'text':sample})
            st.success(f"Predição: **{r['label'].upper()}** | Confiança do modelo: {r['confidence']:.1%}")
            probs=pd.DataFrame([{'Classe':k.title(),'Probabilidade':v} for k,v in r['probabilities'].items()])
            st.bar_chart(probs.set_index('Classe'),height=220)
            st.caption(r['note'])
        except Exception as e: st.error(str(e))
    with st.expander('Como funciona?'):
        st.markdown('O texto vira um vetor TF-IDF de palavras e pares de palavras. A regressão logística aprende pesos para as classes positivo, neutro e negativo. Métricas de teste ficam em `artifacts/metrics.json`. A avaliação usa dados **sintéticos**, portanto a precisão obtida não mede desempenho em comentários reais.')

with tabs[2]:
    st.subheader('Assistente com fontes verificáveis')
    st.markdown('Consulta o FAQ e o cardápio. A versão offline retorna trechos relevantes; com LLM opcional, redige uma resposta **a partir desses trechos**.')
    question=st.text_input('Pergunte algo',value='Quais opções veganas existem no cardápio?',max_chars=400)
    if st.button('Consultar informações',type='primary'):
        try:
            r=api_post('/api/ask',{'question':question,'use_llm':llm_flag})
            if r['grounded']:
                st.markdown(r['answer'])
                st.caption('Modo: '+{'offline':'local sem LLM','structured':'consulta ao banco','llm':'LLM com contexto','offline_fallback':'resposta local (LLM indisponível)'}.get(r['mode'],r['mode']))
                st.markdown('**Fontes utilizadas**')
                for s in r['sources']:
                    if s.get('score') is None:
                        st.markdown(f"- `{s['id']}` — {s['title']} (cadastro do cardápio)")
                    else:
                        st.markdown(f"- `{s['id']}` — {s['title']} (similaridade {s['score']:.2f})")
            else:
                st.warning(r['answer'])
        except Exception as e: st.error(str(e))
    st.caption('Busca local baseada em TF-IDF (não usa embeddings neurais). O assistente pode omitir informações ou selecionar trechos incorretos.')

with tabs[3]:
    st.subheader('Cardápio fictício')
    available=api_get('/api/menu')['items']
    categories=['Todas']+sorted(set(p['category'] for p in available))
    ca,cb,cc=st.columns(3)
    category=ca.selectbox('Categoria',categories)
    budget=cb.slider('Preço máximo (R$)',10,100,60)
    veg=cc.checkbox('Somente vegetarianos')
    listing=[p for p in available if (category=='Todas' or p['category']==category) and p['price']<=budget and (not veg or p['vegetarian'])]
    if listing:
        df=pd.DataFrame([{'Produto':p['name'],'Categoria':p['category'],'Preço':fmt_brl(p['price']),'Vegetariano':'Sim' if p['vegetarian'] else 'Não','Vegano':'Sim' if p['vegan'] else 'Não','Lactose indicada':'Sim' if p['contains_lactose'] else 'Não'} for p in listing])
        st.dataframe(df,hide_index=True,use_container_width=True)
    else: st.info('Nenhum produto atende a esses filtros.')
    st.divider();st.subheader('Recomendador por regras transparentes')
    c1,c2,c3=st.columns(3)
    vegan=c1.checkbox('Vegano')
    lactose=c2.checkbox('Evitar ingredientes com lactose')
    spicy=c3.selectbox('Preferência por picância',['Indiferente','Picante','Não picante'])
    if st.button('Recomendar opções'):
        try:
            r=api_post('/api/recommend',{
                'max_price':float(budget),'vegetarian':veg,'vegan':vegan,
                'avoid_lactose':lactose,'spicy':None if spicy=='Indiferente' else spicy=='Picante','top_k':5})
            if not r['items']:st.warning('Nenhum produto atende a todos os critérios.')
            for p in r['items']:
                st.markdown(f"**{p['name']} — {fmt_brl(p['price'])}**  \n{p['description']}  \n*{p['why_recommended']}*")
            st.caption(r['notice'])
        except Exception as e:st.error(str(e))

with tabs[4]:
    st.subheader('Registrar uma avaliação de demonstração')
    opts=api_get('/api/menu')['items']
    by_name={f"{p['id']} — {p['name']}":p['id'] for p in opts}
    with st.form('review_form',clear_on_submit=True):
        chosen=st.selectbox('Produto avaliado',list(by_name))
        rating=st.slider('Nota',1,5,4)
        text=st.text_area('Avaliação',max_chars=1000,placeholder='Escreva uma avaliação fictícia...')
        submitted=st.form_submit_button('Registrar e classificar',type='primary')
    if submitted:
        try:
            saved=api_post('/api/reviews',{'product_id':by_name[chosen],'rating':rating,'text':text})
            st.success(f"Avaliação #{saved['review']['id']} registrada com sentimento '{saved['prediction']['label']}'.")
        except Exception as e:st.error(str(e))
    st.subheader('Últimas avaliações')
    rows=api_get('/api/reviews?limit=30')['reviews']
    if rows:
        st.dataframe(pd.DataFrame([{'Produto':x['product_name'],'Nota':x['rating'],'Avaliação':x['text'],'Sentimento':x['sentiment']} for x in rows]),hide_index=True,use_container_width=True)

st.divider()
st.caption('Protótipo educacional de portfólio • Não processa pagamentos ou pedidos reais • Dados inteiramente fictícios')

"""API REST para dashboard, ML e assistente com fontes."""
from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from .db import seed, products, product_by_id, get_reviews, add_review, analytics
from .ml import predict, get_model
from .assistant import answer
from .recommend import recommend

@asynccontextmanager
async def lifespan(app: FastAPI):
    seed(); get_model()
    yield

app=FastAPI(title='Projeto de IA — API',version='1.0.0',description='API acadêmica: dados sintéticos e IA explicável',lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=['http://localhost:8501','http://127.0.0.1:8501'],
                   allow_credentials=False,allow_methods=['GET','POST'],allow_headers=['Content-Type'])

class SentimentRequest(BaseModel):
    text:str=Field(min_length=3,max_length=1000)

class ReviewRequest(BaseModel):
    product_id:Optional[int]=Field(default=None,gt=0)
    rating:int=Field(ge=1,le=5)
    text:str=Field(min_length=5,max_length=1000)

class AskRequest(BaseModel):
    question:str=Field(min_length=3,max_length=400)
    use_llm:bool=False

class RecommendRequest(BaseModel):
    max_price:Optional[float]=Field(default=None,ge=0,le=1000)
    vegetarian:bool=False
    vegan:bool=False
    avoid_lactose:bool=False
    spicy:Optional[bool]=None
    top_k:int=Field(default=5,ge=1,le=20)

@app.get('/api/health')
def health():
    return {'status':'ok','version':'1.0.0','data':'synthetic','model':'tfidf-logistic-regression'}

@app.get('/api/menu')
def menu(category:Optional[str]=None,max_price:Optional[float]=Query(None,ge=0),
         vegetarian:Optional[bool]=None, vegan:Optional[bool]=None):
    return {'items':products(category=category,max_price=max_price,vegetarian=vegetarian,vegan=vegan)}

@app.get('/api/reviews')
def reviews(limit:int=Query(100,ge=1,le=500)):
    return {'reviews':get_reviews(limit)}

@app.post('/api/reviews',status_code=201)
def create_review(payload:ReviewRequest):
    if payload.product_id is not None and not product_by_id(payload.product_id):
        raise HTTPException(status_code=404,detail='Produto inexistente')
    sentiment=predict(payload.text)
    saved=add_review(payload.product_id,payload.rating,payload.text,sentiment['label'])
    return {'review':saved,'prediction':sentiment}

@app.get('/api/analytics')
def get_analytics():
    return analytics()

@app.post('/api/sentiment')
def sentiment(payload:SentimentRequest):
    return predict(payload.text)

@app.post('/api/ask')
def ask(payload:AskRequest):
    return answer(payload.question,use_llm=payload.use_llm)

@app.post('/api/recommend')
def recommendations(payload:RecommendRequest):
    return {'items':recommend(max_price=payload.max_price,vegetarian=payload.vegetarian,
                              vegan=payload.vegan,avoid_lactose=payload.avoid_lactose,
                              spicy=payload.spicy,top_k=payload.top_k),
             'notice':'Filtros usam cadastro fictício; informações de alergia precisam confirmação direta.'}

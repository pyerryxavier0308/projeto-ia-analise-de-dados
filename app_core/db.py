"""Camada SQLite: dados de demonstração e consultas parametrizadas."""
import csv
import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from .config import ROOT, db_path
from .formatters import format_brl

SCHEMA = """
CREATE TABLE IF NOT EXISTS menu (
 id INTEGER PRIMARY KEY,
 name TEXT NOT NULL, category TEXT NOT NULL, description TEXT NOT NULL,
 ingredients TEXT NOT NULL, price REAL NOT NULL CHECK(price >= 0),
 vegan INTEGER NOT NULL, vegetarian INTEGER NOT NULL, contains_lactose INTEGER NOT NULL,
 spicy INTEGER NOT NULL, available INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS reviews (
 id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER,
 rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
 text TEXT NOT NULL, sentiment TEXT NOT NULL CHECK(sentiment IN ('positivo','neutro','negativo')),
 created_at TEXT NOT NULL DEFAULT (datetime('now')),
 FOREIGN KEY(product_id) REFERENCES menu(id)
);
CREATE TABLE IF NOT EXISTS knowledge (
 id TEXT PRIMARY KEY, title TEXT NOT NULL, content TEXT NOT NULL, kind TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_reviews_product ON reviews(product_id);
CREATE INDEX IF NOT EXISTS idx_reviews_sentiment ON reviews(sentiment);
"""

@contextmanager
def connection():
    path = db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(str(path), timeout=10)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def seed() -> dict:
    """Criação idempotente: não sobrescreve avaliações já cadastradas."""
    with connection() as db:
        db.executescript(SCHEMA)
        if db.execute('SELECT COUNT(*) FROM menu').fetchone()[0] == 0:
            with (ROOT/'data'/'menu.csv').open(encoding='utf-8', newline='') as f:
                rows = list(csv.DictReader(f))
            db.executemany("""INSERT INTO menu
                (id,name,category,description,ingredients,price,vegan,vegetarian,contains_lactose,spicy,available)
                VALUES (:id,:name,:category,:description,:ingredients,:price,:vegan,:vegetarian,:contains_lactose,:spicy,:available)""",rows)
        if db.execute('SELECT COUNT(*) FROM reviews').fetchone()[0] == 0:
            with (ROOT/'data'/'reviews_demo.csv').open(encoding='utf-8', newline='') as f:
                rows = list(csv.DictReader(f))
            db.executemany('INSERT INTO reviews(product_id,rating,text,sentiment) VALUES (:product_id,:rating,:text,:sentiment)', rows)
        if db.execute('SELECT COUNT(*) FROM knowledge').fetchone()[0] == 0:
            docs = json.loads((ROOT/'data'/'faq.json').read_text(encoding='utf-8'))
            db.executemany('INSERT INTO knowledge(id,title,content,kind) VALUES (:id,:title,:content,:kind)', docs)
        return {
           'products':db.execute('SELECT COUNT(*) FROM menu').fetchone()[0],
           'reviews':db.execute('SELECT COUNT(*) FROM reviews').fetchone()[0],
           'documents':db.execute('SELECT COUNT(*) FROM knowledge').fetchone()[0]
        }

def products(category=None, max_price=None, vegetarian=None, vegan=None, no_lactose=None, only_available=True):
    query = 'SELECT * FROM menu WHERE 1=1'
    args = []
    for clause,value in [('category = ?',category),('price <= ?',max_price),('vegetarian = ?',int(vegetarian) if vegetarian is not None else None),('vegan = ?',int(vegan) if vegan is not None else None),('contains_lactose = ?',0 if no_lactose else None)]:
        if value is not None:
            query += ' AND ' + clause; args.append(value)
    if only_available:
        query += ' AND available = 1'
    query += ' ORDER BY category,name'
    with connection() as db:
        return [dict(x) for x in db.execute(query,args).fetchall()]

def product_by_id(product_id):
    with connection() as db:
        row=db.execute('SELECT * FROM menu WHERE id=?',(product_id,)).fetchone()
        return dict(row) if row else None

def docs_for_retrieval():
    with connection() as db:
        faq = [dict(x) for x in db.execute('SELECT id,title,content,kind FROM knowledge').fetchall()]
        items = [dict(x) for x in db.execute('SELECT * FROM menu WHERE available=1').fetchall()]
    result=faq[:]
    for p in items:
        tags=[]
        if p['vegan']: tags.append('vegano')
        if p['vegetarian']: tags.append('vegetariano')
        if p['contains_lactose']: tags.append('contém lactose')
        else: tags.append('sem ingredientes com lactose identificados; confirmar contaminação cruzada')
        if p['spicy']: tags.append('picante')
        result.append({'id':f"menu:{p['id']}",'title':p['name'],'kind':'cardapio',
          'content':f"{p['name']}. {p['description']}. Categoria: {p['category']}. Ingredientes: {p['ingredients']}. Preço: {format_brl(p['price'])}. Características: {', '.join(tags)}."})
    return result

def add_review(product_id, rating, text, sentiment):
    with connection() as db:
        cur=db.execute('INSERT INTO reviews(product_id,rating,text,sentiment) VALUES (?,?,?,?)', (product_id,rating,text,sentiment))
        rid=cur.lastrowid
        return dict(db.execute('SELECT * FROM reviews WHERE id=?',(rid,)).fetchone())

def get_reviews(limit=100):
    with connection() as db:
        return [dict(r) for r in db.execute("""SELECT r.id,r.rating,r.text,r.sentiment,r.created_at,r.product_id,m.name AS product_name
             FROM reviews r LEFT JOIN menu m ON m.id=r.product_id ORDER BY r.id DESC LIMIT ?""",(limit,)).fetchall()]

def analytics():
    with connection() as db:
        total=db.execute('SELECT COUNT(*),AVG(rating) FROM reviews').fetchone()
        sent={r['sentiment']:r['n'] for r in db.execute('SELECT sentiment,COUNT(*) n FROM reviews GROUP BY sentiment')}
        by_product=[dict(r) for r in db.execute("""SELECT m.name, COUNT(r.id) as reviews, ROUND(AVG(r.rating),2) as avg_rating
                      FROM menu m LEFT JOIN reviews r ON m.id=r.product_id
                      GROUP BY m.id ORDER BY reviews DESC, m.name""")]
    return {'total_reviews':total[0],'average_rating':round(total[1] or 0,2),
            'sentiment_counts':{k:sent.get(k,0) for k in ('positivo','neutro','negativo')},
            'by_product':by_product}

"""Recomendador explicável por filtros e ordenação (sem Machine Learning)."""
from .db import products
from .formatters import format_brl

def recommend(max_price=None, vegetarian=False, vegan=False, avoid_lactose=False, spicy=None, top_k=5):
    items = products(max_price=max_price, vegetarian=True if vegetarian else None,
                     vegan=True if vegan else None, no_lactose=True if avoid_lactose else None)
    if spicy is not None:
        items = [p for p in items if bool(p['spicy']) == spicy]
    result = []
    for p in sorted(items, key=lambda p: (p['price'], p['name']))[:top_k]:
        reasons = []
        if vegan:
            reasons.append('classificado como vegano no cadastro fictício')
        elif vegetarian:
            reasons.append('classificado como vegetariano no cadastro fictício')
        if avoid_lactose:
            reasons.append('sem ingrediente com lactose indicado no cadastro')
        if spicy is True:
            reasons.append('cadastrado como picante')
        elif spicy is False:
            reasons.append('cadastrado como não picante')
        if max_price is not None:
            reasons.append(f'preço dentro do limite de {format_brl(max_price)}')
        if not reasons:
            reasons.append('disponível no cardápio fictício')
        result.append({**p, 'why_recommended': '; '.join(reasons).capitalize() + '. Ordenado por preço crescente.'})
    return result

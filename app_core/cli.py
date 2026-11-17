"""Comandos utilitários: python -m app_core.cli init|train|demo."""
import argparse
import json
from .db import seed
from .ml import train
from .assistant import answer

def main():
    p=argparse.ArgumentParser(description='Projeto de IA — Análise de Dados utilitários')
    p.add_argument('command',choices=['init','train','demo'])
    args=p.parse_args()
    if args.command=='init': print(json.dumps(seed(),ensure_ascii=False,indent=2))
    elif args.command=='train': print(json.dumps(train(),ensure_ascii=False,indent=2))
    else:
        seed(); print(json.dumps(answer('Quais são as opções veganas?'),ensure_ascii=False,indent=2))

if __name__=='__main__':main()

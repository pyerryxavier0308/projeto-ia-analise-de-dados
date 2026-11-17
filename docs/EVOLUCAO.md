# Roadmap para evolução do projeto

## Já implementado

- API REST; SQLite; validação com Pydantic.
- Dashboard Streamlit; classificação com TF-IDF e regressão logística.
- Busca textual com evidências; adaptação opcional para LLM externo.
- Recomendações por filtros explícitos; testes automatizados.

## Próximos incrementos recomendados

1. **Paginação e ordenação:** incluir paginação e ordenação na lista de avaliações, com testes.
2. **Qualidade de ML:** usar dados externos reais com licença compatível; manter o split por grupos de template e acrescentar um conjunto real externo para evitar avaliação otimista; registrar experimentos.
3. **RAG melhor:** incorporar embeddings neurais locais e índice FAISS ou Chroma; medir recall@k, precisão e groundedness em um conjunto de questões.
4. **Segurança:** autenticação e limite de requisições, proteção de dados pessoais, varredura de segredos e logs sanitizados.
5. **Deploy:** banco PostgreSQL, migrações SQL, pipeline CI, hospedagem e monitoramento.
6. **Agentes:** adicionar tool-calling controlado para consultar menu, avaliar recomendações e registrar eventos, com autorização explícita e sem pedidos reais.
7. **Experiência:** melhorar acessibilidade e testes de interface, criar relatório de arquitetura e vídeo de demonstração.

## Escopo intencionalmente fora do MVP

Pedidos reais, integração com plataformas de entrega, pagamentos, ingestão de dados privados, avaliação de alergias para consumo e qualquer alegação de vínculo com empresas.

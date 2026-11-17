# Como apresentar o projeto em uma entrevista

## Resumo técnico de 45 segundos

> O Projeto de IA — Análise de Dados é um protótipo educacional para análise de avaliações e consultas a um cardápio fictício. Integra API FastAPI, banco SQLite e dashboard Streamlit. Utiliza TF-IDF e regressão logística para classificar sentimentos, com métricas de avaliação. Inclui ainda um assistente de recuperação de informação que apresenta as fontes consultadas, integração opcional com LLM externo e recomendação baseada em regras. A arquitetura permite estudar a integração entre interface, API, banco, modelos e testes automatizados.

## Perguntas técnicas frequentes

**Por que TF-IDF?** Transforma textos em vetores ponderados por frequência e raridade das palavras. É um baseline barato e interpretável; não capta todo o contexto como um embedding neural.

**Por que regressão logística para sentimento?** É um classificador supervisionado simples que fornece probabilidades por classe e serve como baseline. Dados de treino rotulados são necessários.

**O que significam precision, recall e F1?** Precision mede a proporção de positivos previstos que de fato são positivos; recall mede a proporção dos positivos reais identificados; F1 harmoniza os dois. Devem ser calculados por classe em tarefas multiclasse.

**O que é leakage?** Quando informações da validação/teste vazam para o treino, produzindo métricas artificialmente boas. Os exemplos aqui são artificiais e variantes de templates, por isso usamos separação por grupos de templates; mesmo assim, sem dados reais, a métrica pode ser otimista.

**Isto é RAG?** É uma forma simplificada de recuperação + geração opcional. No modo sem LLM, faz recuperação e mostra trechos, sem geração. No modo LLM externo, a resposta é produzida com contexto recuperado. O sistema não usa embeddings neurais nem banco vetorial dedicado.

**Como reduzir alucinações?** Limitar fontes, citar evidências, responder 'não sei' quando não houver fonte confiável, avaliar respostas e evitar confiar apenas na instrução do prompt.

**O recomendador usa ML?** Não. Aplica filtros e ordenação explícitos. Uma evolução seria um modelo de ranking com feedback e avaliação off-line/on-line.

**Como funciona o banco?** O SQLite guarda cardápio, avaliações e FAQ. As consultas usam placeholders `?`, não interpolação de SQL, para evitar injeção.

**Como colocaria em produção?** Adicionaria autenticação, autorização, HTTPS, logging sem dados sensíveis, testes de carga, monitoramento, banco mais robusto, controle de requisições e avaliação de dados reais com consentimento e licença.

## Tópicos para demonstração técnica

- Fluxo entre interface Streamlit, endpoints FastAPI, SQLite e classificador.
- Preparação dos dados, separação por grupos, TF-IDF e regressão logística.
- Significado das métricas e limitações do treinamento sintético.
- Demonstração dos endpoints na documentação Swagger.
- Distinção entre recuperação lexical de documentos e um chatbot com modelo generativo.
- Funcionamento do recomendador por regras explícitas.
- Limites de segurança, dados fictícios e possibilidades de evolução do sistema.

# Projeto de IA — Análise de Dados e Recomendações

**Projeto educacional independente para estudo e portfólio em IA e dados.** Protótipo em Python que integra Machine Learning, análise de avaliações, API REST, banco de dados, busca de informações com fontes e dashboard interativo.

> **Aviso:** todos os restaurantes, pratos, preços e avaliações são **fictícios**. A aplicação não recebe pedidos nem pagamentos reais e não deve ser usada para decidir sobre alergias ou segurança alimentar.

## Funcionalidades

| Recurso | Tecnologias | Como funciona |
|---|---|---|
| Classificação de sentimento | scikit-learn, TF-IDF, regressão logística | Treina um modelo com avaliações sintéticas para prever positivo, neutro ou negativo |
| Dashboard de avaliações | Streamlit, pandas | Quantidade, nota média, distribuição de classes e produtos |
| Assistente de cardápio | TF-IDF, similaridade de cosseno | Recupera fatos do cardápio e do FAQ e informa **as fontes utilizadas** |
| Resposta de LLM (opcional) | API OpenAI | Redige uma resposta a partir dos fatos encontrados; **exige chave e pode gerar custo** |
| Recomendações | Regras de negócio | Filtra por preço, dieta, lactose cadastrada e picância — **não é recomendação por ML** |
| API | FastAPI, Pydantic | Valida entradas, retorna JSON e expõe documentação automática |
| Persistência | SQLite | Mantém pratos e avaliações e aceita novas avaliações de demonstração |
| Testes | pytest, TestClient | Exercitam a API, validações, banco e pipeline de ML |

## Iniciar no Windows (Python 3.13)

**Jeito mais fácil:** extraia a pasta do ZIP, entre nela e dê dois cliques em `run_windows.bat`. O script cria `.venv`, instala as dependências, inicializa os dados, treina o modelo e abre dois processos: API e dashboard.

Se preferir executar manualmente pelo **terminal PowerShell do VS Code**, dentro da pasta do projeto:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m app_core.cli init
python -m app_core.cli train
python -m uvicorn app_core.api:app --reload
```

Abra **um segundo terminal** na mesma pasta, ative o ambiente e execute:

```powershell
.\.venv\Scripts\Activate.ps1
python -m streamlit run dashboard/app.py
```

- **Dashboard:** <http://localhost:8501>
- **Documentação da API (Swagger):** <http://127.0.0.1:8000/docs>
- **Status da API:** <http://127.0.0.1:8000/api/health>

Se PowerShell bloquear a ativação, use o executável diretamente: `.\.venv\Scripts\python.exe -m ...`. Não é necessário alterar a política global do Windows.

### Linux / macOS

```bash
sh run_linux_mac.sh
```

### Docker (opcional)

```bash
docker compose up --build
```

## Como usar

1. Na aba **Visão geral**, explore o resumo das avaliações fictícias e o ranking de produtos.
2. Na aba **Análise de sentimento**, escreva uma avaliação para ver a classificação e as probabilidades.
3. Na aba **Assistente**, pergunte *“Qual é o horário?”* ou *“Vocês têm opções veganas?”*. Confira a lista de fontes.
4. Em **Cardápio**, filtre os itens e peça sugestões por restrições cadastradas.
5. Em **Avaliações**, registre uma avaliação e observe a atualização dos indicadores.

## Estrutura do projeto

```text
projeto-ia-analise-dados/
├── app_core/              # API, banco, ML, retrieval e regras de negócio
│   ├── api.py
│   ├── assistant.py
│   ├── db.py
│   ├── ml.py
│   ├── retrieval.py
│   ├── recommend.py
│   └── cli.py
├── dashboard/app.py       # Interface Streamlit
├── data/                  # CSV/JSON sintéticos de exemplo
├── tests/                 # Testes automatizados
├── docs/                  # Arquitetura, limitações e entrevista
├── requirements.txt
├── requirements-dev.txt
├── requirements-llm.txt
├── run_windows.bat
├── run_linux_mac.sh
└── docker-compose.yml
```

O diretório `artifacts/` é gerado na primeira execução e ignorado pelo Git: contém o banco SQLite, o modelo treinado e `metrics.json`. Nunca carregue modelos serializados de fontes desconhecidas com `joblib`.

## Treinar e avaliar o modelo

```powershell
python -m app_core.cli train
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

O treinamento usa separação de treino/teste por **grupos de templates** (`StratifiedGroupKFold`, `random_state=42`). As métricas incluem acurácia, precision, recall, F1 e matriz de confusão, salvas em `artifacts/metrics.json`.

**Limite crítico:** o dataset é pequeno e **sintético**, gerado com padrões semelhantes. Uma boa acurácia nele **não garante** funcionamento em comentários reais. Uma evolução importante é coletar dados externos com licença apropriada e avaliar em um conjunto verdadeiramente independente.

## Busca fundamentada (RAG simplificado)

Para perguntas abertas, a pergunta é transformada em TF-IDF; com similaridade de cosseno são recuperados documentos do FAQ e descrições do cardápio. Sem LLM, o sistema **mostra trechos relevantes**, e não gera texto criativo. Se uma fonte adequada não for encontrada, deve informar que os dados não são suficientes. Perguntas sobre pedidos e entregadores reais recebem recusa contextual. Listas de opções veganas e vegetarianas usam consulta estruturada ao SQLite.

Opcionalmente, com `OPENAI_API_KEY` configurada e `openai` instalado (`pip install -r requirements-llm.txt`), o backend pode gerar uma resposta usando o contexto recuperado. Essa integração envia a pergunta e o contexto ao provedor externo e pode ter cobrança; não use dados pessoais reais.

O TF-IDF **não é embedding neural**, não faz busca semântica de nível de produção e pode selecionar documentos incompletos. A presença de fontes tampouco garante que uma resposta gerada esteja correta.

## Notas de interface e limites

- Valores monetários são exibidos em reais com separador decimal brasileiro.
- O filtro de **vegetarianos** inclui itens com ovos ou leite, enquanto **vegano** é uma classificação distinta do cadastro fictício. A tabela apresenta ambas.
- O recomendador aplica filtros explícitos e explica os critérios atendidos; não é um modelo de ML.
- As fontes de consultas diretas ao cardápio são identificadas como cadastro, sem pontuação fictícia de similaridade.
- A classificação de sentimento é um baseline treinado com textos sintéticos; sua confiança estimada não garante acerto.

## Segurança e escopo

- Não adicionar `.env`, chaves, banco gerado nem `.venv` ao GitHub.
- A API foi pensada para uso local, sem autenticação de usuários ou limitação de requisições.
- Os alimentos, ingredientes e indicações de lactose são fictícios e não incluem risco de contaminação cruzada.
- Não exponha essa API sem acrescentar autenticação, limitação de requisições, logs seguros e controle de acesso.
- As avaliações que você digitar são gravadas localmente; use apenas conteúdo fictício.

## Documentação complementar

- [Arquitetura e decisões técnicas](docs/ARQUITETURA.md)
- [Roteiro para explicar o projeto em entrevistas](docs/ENTREVISTA.md)
- [Limitações e melhorias futuras](docs/EVOLUCAO.md)

## Autoria

Projeto independente desenvolvido para fins de estudo, aprendizado prático e composição de portfólio na área de Inteligência Artificial e Análise de Dados.

O desenvolvimento contou com o auxílio de ferramentas de IA na implementação e documentação, seguido de execução, testes, ajustes e validação das funcionalidades.

## Licença

MIT (ver `LICENSE`).

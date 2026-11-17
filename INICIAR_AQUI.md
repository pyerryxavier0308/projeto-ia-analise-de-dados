# Comece por aqui — Projeto de IA — Análise de Dados

Esta pasta já contém **o projeto completo para execução local**, não apenas um roteiro. Todos os dados são fictícios.

## No Windows 10/11 com Python 3.13

1. Extraia o ZIP para uma pasta simples, por exemplo `Documentos\Projetos\projeto-ia-analise-dados`.
2. Abra essa pasta no VS Code (**File → Open Folder**).
3. Execute o arquivo `run_windows.bat` (duplo clique pelo Explorador de Arquivos), **ou** siga os comandos manuais descritos no `README.md`.
4. As duas janelas de terminal iniciam API e dashboard; mantenha ambas abertas.
5. Abra <http://localhost:8501>. A documentação da API fica em <http://127.0.0.1:8000/docs>.

**Instalação inicial:** requer internet para instalar dependências do Python. Após a instalação, o modo local funciona sem chave de API.

## Teste inicial sugerido

- [ ] Abri a aba **Visão geral** e vi indicadores e gráfico.
- [ ] Classifiquei o texto “A pizza estava deliciosa e chegou quentinha”.
- [ ] Perguntei ao assistente “Quais opções veganas existem?”.
- [ ] Perguntei “Qual a capital da França?” e confirmei que não inventa resposta.
- [ ] Filtrei itens do cardápio e pedi uma recomendação.
- [ ] Cadastrei uma avaliação fictícia e conferi se o total aumentou.
- [ ] Rodei `python -m pytest -q` após instalar `requirements-dev.txt`.

## Verificações realizadas

- **Testes automatizados:** 17 testes passaram no ambiente de desenvolvimento e novamente na instalação Windows, com um aviso de depreciação de dependência.
- **Sintaxe Python:** verificada na compilação.
- **Treinamento de ML:** executado no Windows, com acurácia aproximada de 54,35% nos dados sintéticos de avaliação.
- **API e dashboard:** execução local confirmada no Windows.
- **Assistente e recomendador:** formatação das fontes, preços e justificativas verificada na interface.
- **Integração opcional com LLM e Docker:** execução não verificada.

## Estado da versão

O projeto contém código, dados fictícios, documentação e testes automatizados. As limitações do classificador e os requisitos para uso fora do ambiente local estão descritos no `README.md` e em `docs/EVOLUCAO.md`.
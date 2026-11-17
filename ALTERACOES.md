# Alterações nesta versão

- O título exibido passou a ser **Projeto de IA — Análise de Dados** (sem nome comercial). A pasta interna Python agora se chama `app_core`.
- O subtítulo da barra lateral é **Laboratório de IA e dados**, e a referência a qualquer empresa foi removida.
- Consultas estruturadas ao cardápio exibem os itens como lista Markdown, com preços em `R$ 31,50`, e a lista de fontes não usa similaridade inventada.
- A tabela do cardápio agora diferencia **vegetariano** de **vegano**.
- O recomendador explica cada condição atendida, usando os rótulos fictícios cadastrados.
- Os preços na interface e nas respostas estruturadas são exibidos no formato brasileiro.
- Mantida a correção que recusa informar pedidos reais/entregadores.
- README, exemplos, scripts de execução, Docker e testes foram atualizados para o novo nome técnico.
- Foram adicionados testes para preço, recomendação, listagem de fontes e pedidos pessoais.

## Limitações conhecidas

O classificador de sentimentos é um modelo inicial treinado com exemplos artificiais; o conjunto de dados não foi ampliado nem reavaliado nesta atualização. A interface atualizada foi executada e conferida no Windows, e os 17 testes automatizados passaram. A integração opcional com LLM externo e a execução via Docker permanecem sem validação.

## Como testar esta versão

As instruções de instalação e migração estão em `INICIAR_AQUI.md`. A versão utiliza `app_core`, estrutura diferente da edição inicial. A `.venv` e o banco gerado localmente não acompanham a distribuição.

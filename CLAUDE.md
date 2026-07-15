\# Contexto do Projeto para Claude / Claude Code / Cowork



Este arquivo existe para que qualquer sessão de IA (Claude no chat, Claude

Code, Cowork) entenda rapidamente o projeto sem precisar reler todo o

histórico de conversas.



\## Leitura obrigatória antes de qualquer alteração

1\. `docs/handoff/current-state.md` — estado atual

2\. `docs/handoff/next-steps.md` — próximo passo combinado

3\. `docs/decisions/decision-log.md` — decisões já aprovadas (não reverter

&#x20;  sem confirmar com o usuário)



\## Regras fixas deste projeto

\- Nunca usar dados reais de hóspedes em código, testes ou exemplos.

\- Nunca commitar o arquivo `.env` (ver `.gitignore`).

\- Preferir poucas alterações por vez; não editar dezenas de arquivos de uma

&#x20; vez sem aprovação explícita do usuário.

\- Recomendar um commit de segurança antes de alterações estruturais.

\- Não alterar stack, arquitetura ou identidade visual sem justificar e

&#x20; obter aprovação.

\- Confiabilidade dos dados de vipagem é a prioridade máxima do projeto.



\## Stack

Python, Flask, HTML/CSS/JS, banco relacional via SQLAlchemy, Flask-Migrate,

Flask-Login, openpyxl. Front-end com identidade editorial maximalista

(ver `docs/design/design-system.md` quando definido).


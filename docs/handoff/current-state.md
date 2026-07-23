\# Estado Atual do Projeto — Plataforma de Guest Relations



\*\*Última atualização:\*\* 2026-07-23



\## Fase atual

Planejamento inicial. Nenhum código foi escrito ainda. A modelagem foi concluída e a implementação do banco (SQLAlchemy) é o próximo passo.



\## O que já existe

\- Documentos de produto e decisões (docs/product/vision.md,

&#x20; docs/product/backlog.md, docs/decisions/decision-log.md).

\- Escopo definido: MVP, pós-MVP e integrações futuras (ver backlog.md).

\- Stack tecnológica definida (ver decision-log.md).

\- Identidade visual editorial definida (fundo off-white, Manrope, Instrument

&#x20; Serif, acentos coloridos, cards em camadas) — ainda não aplicada em

&#x20; nenhuma tela, pois nenhuma tela foi criada.

- Modelo de dados completo aprovado e documentado em
  docs/technical/data-model.md (6 tabelas: User, Guest, Reservation,
  VipPlan, VipItem, AuditLog).
- Modelo de dados completo aprovado e documentado (6 tabelas: User, Guest,
  Reservation, VipPlan, VipItem, AuditLog) — ver docs/technical/data-model.md.
- Ambiente Python local funcional (venv + Flask mínimo testado com sucesso).


\## O que NÃO existe ainda

\- Repositório Git/GitHub.
\- Estrutura de pastas do código.
\- Aplicação Flask.
\- Banco de dados/modelos.
\- Autenticação.
\- Qualquer tela ou protótipo no Figma Make.
- Nenhum model SQLAlchemy implementado (próximo passo).
- Nenhuma migração de banco de dados criada.



\## Como retomar o trabalho

1\. Leia este arquivo e `docs/handoff/next-steps.md`.

2\. Leia `docs/decisions/decision-log.md` para não repetir decisões já

&#x20;  tomadas.

3\. Confirme com o usuário se algo mudou desde a última atualização deste

&#x20;  arquivo antes de prosseguir.


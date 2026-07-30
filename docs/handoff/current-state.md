\# Estado Atual do Projeto — Plataforma de Guest Relations



\*\*Última atualização:\*\* 2026-07-30



\## Fase atual

Implementação dos models do banco de dados. A modelagem está concluída e
aprovada; os models estão sendo implementados um a um, cada um com sua
migração. Já implementados: User, Guest e Reservation. Próximo: VipPlan.



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

- Aplicação Flask reestruturada em pacote (app/), com application factory
  (create_app()).
- SQLAlchemy e Flask-Migrate configurados e funcionando.
- Models implementados: User, Guest, Reservation.
- Primeira migração aplicada; banco SQLite local funcional
  (instance/plataforma_gr.db, fora do controle de versão).
- Model Reservation criado em app/models/reservation.py (FK guest_id ->
  guests.id, reservation_code único, source com default "manual"),
  registrado em app/models/__init__.py.
- Migração "Cria tabela de reservas" gerada e aplicada com sucesso; a
  tabela reservations existe no banco (confirmado via inspect: tabelas
  atuais = alembic_version, guests, reservations, users).
- Decisões sobre os campos em aberto de Reservation (source, room_number,
  reservation_code) registradas em docs/decisions/decision-log.md,
  entrada de 2026-07-30.


\## O que NÃO existe ainda

\- Autenticação (Flask-Login).
\- Qualquer tela ou protótipo no Figma Make.
- Models VipPlan, VipItem e AuditLog (VipPlan é o próximo passo).
- Qualquer rota, view ou template da aplicação.
- Exportação em XLSX.



\## Como retomar o trabalho

1\. Leia este arquivo e `docs/handoff/next-steps.md`.

2\. Leia `docs/decisions/decision-log.md` para não repetir decisões já

&#x20;  tomadas.

3\. Confirme com o usuário se algo mudou desde a última atualização deste

&#x20;  arquivo antes de prosseguir.


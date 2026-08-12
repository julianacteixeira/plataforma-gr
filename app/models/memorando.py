from datetime import datetime, timezone
from app.extensions import db


class Memorando(db.Model):
    __tablename__ = "memorandos"

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)
    vip_plan_id = db.Column(
        db.Integer, db.ForeignKey("vip_plans.id"), nullable=True
    )
    version_number = db.Column(db.Integer, nullable=False, default=1)
    previous_version_id = db.Column(
        db.Integer, db.ForeignKey("memorandos.id"), nullable=True
    )
    status_versao = db.Column(db.String(20), nullable=False)
    responsavel_interno_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    generated_by_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    generated_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    data_pedido = db.Column(db.Date, nullable=False)
    observacao = db.Column(db.Text, nullable=True)
    exported_at = db.Column(db.DateTime, nullable=True)
    forma_pagamento = db.Column(db.String(50), nullable=True)
    valor_total = db.Column(db.Numeric(10, 2), nullable=True)
    pax_adultos = db.Column(db.Integer, nullable=True)
    pax_criancas_6_12 = db.Column(db.Integer, nullable=True)
    pax_criancas_ate_5 = db.Column(db.Integer, nullable=True)

    vip_plan = db.relationship("VipPlan")
    previous_version = db.relationship("Memorando", remote_side=[id])
    responsavel_interno = db.relationship(
        "User", foreign_keys=[responsavel_interno_id]
    )
    generated_by = db.relationship("User", foreign_keys=[generated_by_id])

    def __repr__(self):
        return f"<Memorando {self.id} {self.tipo} v{self.version_number}>"

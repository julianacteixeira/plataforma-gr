from datetime import datetime, timezone
from sqlalchemy import event
from app.extensions import db


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    entity_type = db.Column(db.String(50), nullable=False)
    entity_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(50), nullable=False)
    details = db.Column(db.Text, nullable=False)
    timestamp = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    user = db.relationship("User")

    def __repr__(self):
        return f"<AuditLog {self.id} {self.entity_type}:{self.entity_id}>"


@event.listens_for(AuditLog, "before_update")
def block_audit_log_update(mapper, connection, target):
    raise RuntimeError("Entradas de AuditLog não podem ser alteradas.")


@event.listens_for(AuditLog, "before_delete")
def block_audit_log_delete(mapper, connection, target):
    raise RuntimeError("Entradas de AuditLog não podem ser apagadas.")

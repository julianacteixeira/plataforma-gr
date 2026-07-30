from datetime import datetime, timezone
from app.extensions import db


class VipPlan(db.Model):
    __tablename__ = "vip_plans"

    id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(
        db.Integer, db.ForeignKey("reservations.id"), nullable=False
    )
    planned_date = db.Column(db.Date, nullable=False)
    room_number_override = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(30), nullable=False)
    delivery_status = db.Column(db.String(30), nullable=False)
    delivered_at = db.Column(db.DateTime, nullable=True)
    delivered_by_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=True
    )
    created_by_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    delivered_by = db.relationship("User", foreign_keys=[delivered_by_id])
    created_by = db.relationship("User", foreign_keys=[created_by_id])

    def __repr__(self):
        return f"<VipPlan {self.id} {self.planned_date}>"

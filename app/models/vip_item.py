from datetime import datetime, timezone
from app.extensions import db


class VipItem(db.Model):
    __tablename__ = "vip_items"

    id = db.Column(db.Integer, primary_key=True)
    vip_plan_id = db.Column(
        db.Integer, db.ForeignKey("vip_plans.id"), nullable=False
    )
    item_type_id = db.Column(
        db.Integer, db.ForeignKey("item_types.id"), nullable=False
    )
    description = db.Column(db.String(255), nullable=True)
    cost = db.Column(db.Numeric(10, 2), nullable=True)
    responsible_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    availability_status = db.Column(db.String(30), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    vip_plan = db.relationship("VipPlan")
    item_type = db.relationship("ItemType")
    responsible = db.relationship("User")

    def __repr__(self):
        return f"<VipItem {self.id} {self.description}>"

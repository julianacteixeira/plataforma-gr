from datetime import datetime, timezone
from app.extensions import db


class ItemType(db.Model):
    __tablename__ = "item_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    default_cost = db.Column(db.Numeric(10, 2), nullable=False)
    cost_category = db.Column(db.String(30), nullable=False)
    assembly_instructions = db.Column(db.Text, nullable=False)
    preparation_sector = db.Column(db.String(30), nullable=True)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<ItemType {self.name}>"

from datetime import datetime, timezone
from app.extensions import db


class Guest(db.Model):
    __tablename__ = "guests"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200), nullable=False)
    document = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    opera_guest_id = db.Column(db.String(50), unique=True, nullable=True)
    vip = db.Column(db.Boolean, default=False, nullable=False)
    all_member = db.Column(db.Boolean, default=False, nullable=False)
    all_card_number = db.Column(db.String(50), nullable=True)
    pmid = db.Column(db.String(50), nullable=True)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<Guest {self.full_name}>"
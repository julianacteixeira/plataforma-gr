from datetime import datetime, timezone
from app.extensions import db


class StayBadge(db.Model):
    __tablename__ = "stay_badges"

    id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(
        db.Integer, db.ForeignKey("reservations.id"), nullable=False
    )
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    source = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    created_by_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=True
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

    reservation = db.relationship("Reservation")
    category = db.relationship("Category")
    created_by = db.relationship("User", foreign_keys=[created_by_id])

    def __repr__(self):
        return f"<StayBadge reservation_id={self.reservation_id} category_id={self.category_id}>"

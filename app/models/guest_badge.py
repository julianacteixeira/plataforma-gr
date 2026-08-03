from datetime import datetime, timezone
from app.extensions import db


class GuestBadge(db.Model):
    __tablename__ = "guest_badges"

    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey("guests.id"), nullable=False)
    label = db.Column(db.String(50), nullable=False)
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

    guest = db.relationship("Guest", foreign_keys=[guest_id])
    created_by = db.relationship("User", foreign_keys=[created_by_id])

    def __repr__(self):
        return f"<GuestBadge {self.label} guest_id={self.guest_id}>"

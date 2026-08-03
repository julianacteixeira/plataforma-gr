from datetime import datetime, timezone
from app.extensions import db


class GuestLink(db.Model):
    __tablename__ = "guest_links"
    __table_args__ = (
        db.UniqueConstraint(
            "primary_guest_id", "secondary_guest_id",
            name="uq_guest_links_primary_secondary",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    primary_guest_id = db.Column(
        db.Integer, db.ForeignKey("guests.id"), nullable=False
    )
    secondary_guest_id = db.Column(
        db.Integer, db.ForeignKey("guests.id"), nullable=False
    )
    created_by_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    primary_guest = db.relationship("Guest", foreign_keys=[primary_guest_id])
    secondary_guest = db.relationship("Guest", foreign_keys=[secondary_guest_id])
    created_by = db.relationship("User", foreign_keys=[created_by_id])

    def __repr__(self):
        return f"<GuestLink primary={self.primary_guest_id} secondary={self.secondary_guest_id}>"

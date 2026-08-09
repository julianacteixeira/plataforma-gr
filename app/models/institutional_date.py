from datetime import datetime, timezone
from app.extensions import db


class InstitutionalDate(db.Model):
    __tablename__ = "institutional_dates"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    created_by_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    created_by = db.relationship("User")

    def __repr__(self):
        return f"<InstitutionalDate {self.name} {self.date}>"

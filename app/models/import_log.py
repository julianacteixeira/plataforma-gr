from datetime import datetime, timezone
from app.extensions import db


class ImportLog(db.Model):
    __tablename__ = "import_logs"

    id = db.Column(db.Integer, primary_key=True)
    imported_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    imported_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    filename = db.Column(db.String(255), nullable=False)
    total_reservations = db.Column(db.Integer, nullable=False)
    total_created = db.Column(db.Integer, nullable=False)
    total_updated = db.Column(db.Integer, nullable=False)
    total_cancelled = db.Column(db.Integer, nullable=False)
    total_errors = db.Column(db.Integer, nullable=False)

    imported_by = db.relationship("User")

    def __repr__(self):
        return f"<ImportLog {self.id} {self.filename}>"

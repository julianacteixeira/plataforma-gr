from app.extensions import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    scope = db.Column(db.String(10), nullable=False)
    group_number = db.Column(db.Integer, nullable=False)
    always_apply = db.Column(db.Boolean, default=False, nullable=False)
    manual_only = db.Column(db.Boolean, default=False, nullable=False)
    suggestion_priority = db.Column(db.Integer, nullable=True)
    active = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<Category {self.name} ({self.scope})>"

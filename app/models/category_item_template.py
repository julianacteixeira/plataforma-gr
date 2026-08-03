from app.extensions import db


class CategoryItemTemplate(db.Model):
    __tablename__ = "category_item_templates"
    __table_args__ = (
        db.UniqueConstraint(
            "category_id", "item_type_id", "requires_child",
            name="uq_category_item_templates_category_item_child",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    item_type_id = db.Column(db.Integer, db.ForeignKey("item_types.id"), nullable=False)
    requires_child = db.Column(db.Boolean, nullable=True)

    category = db.relationship("Category")
    item_type = db.relationship("ItemType")

    def __repr__(self):
        return f"<CategoryItemTemplate category_id={self.category_id} item_type_id={self.item_type_id}>"

from app.extensions import db


class MemorandoLine(db.Model):
    __tablename__ = "memorando_lines"

    id = db.Column(db.Integer, primary_key=True)
    memorando_id = db.Column(
        db.Integer, db.ForeignKey("memorandos.id"), nullable=False
    )
    vip_item_id = db.Column(
        db.Integer, db.ForeignKey("vip_items.id"), nullable=True
    )
    item_type_id = db.Column(
        db.Integer, db.ForeignKey("item_types.id"), nullable=False
    )
    quantidade = db.Column(db.Integer, nullable=False)
    data_entrega = db.Column(db.Date, nullable=False)
    horario = db.Column(db.String(5), nullable=True)
    pax = db.Column(db.Integer, nullable=True)
    descricao_observacao = db.Column(db.Text, nullable=True)

    memorando = db.relationship("Memorando")
    vip_item = db.relationship("VipItem")
    item_type = db.relationship("ItemType")

    def __repr__(self):
        return f"<MemorandoLine {self.id} memorando_id={self.memorando_id}>"

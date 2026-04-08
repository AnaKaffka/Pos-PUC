from .db import db

class Observacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False)
    data = db.Column(db.String(20), nullable=False)
    texto = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'pet_id': self.pet_id,
            'data': self.data,
            'texto': self.texto
        }
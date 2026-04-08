from .db import db

class Diario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False)
    comida_preferida = db.Column(db.String(100), nullable=True)
    veterinario = db.Column(db.String(100), nullable=True)
    data_vacinacao = db.Column(db.String(20), nullable=True)
    peso = db.Column(db.Float, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'pet_id': self.pet_id,
            'comida_preferida': self.comida_preferida,
            'veterinario': self.veterinario,
            'data_vacinacao': self.data_vacinacao,
            'peso': self.peso,
            'observacoes': self.observacoes
        }
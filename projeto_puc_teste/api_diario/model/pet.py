from .db import db

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    foto = db.Column(db.String(200), nullable=True)

    diarios = db.relationship('Diario', backref='pet', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'tipo': self.tipo,
            'foto': self.foto
        }
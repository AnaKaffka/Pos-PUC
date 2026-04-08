from .db import db

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, nullable=False)  # Assuming pet_id from external API
    vet_id = db.Column(db.Integer, db.ForeignKey('vet.id'), nullable=False)
    data = db.Column(db.String(20), nullable=False)
    motivo = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'pet_id': self.pet_id,
            'vet_id': self.vet_id,
            'data': self.data,
            'motivo': self.motivo
        }
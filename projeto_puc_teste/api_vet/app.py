from flask import Flask, request, jsonify
from flask_cors import CORS
from flasgger import Swagger
import requests
from model.db import db
from model.vet import Vet
from model.appointment import Appointment
from schemas.vet_schema import VetCreateSchema, VetResponseSchema
from schemas.appointment_schema import AppointmentCreateSchema, AppointmentResponseSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
db.init_app(app)
swagger = Swagger(app)

with app.app_context():
    db.create_all()

# ------------------------- 
# Rotas VET
# -------------------------
@app.route("/vets", methods=["POST"])
def cadastrar_vet():
    """
    Cadastrar um novo veterinário
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/VetCreate'
    responses:
      201:
        description: Veterinário cadastrado
    """
    dados = request.json
    schema = VetCreateSchema(**dados)
    vet = Vet(**schema.dict())
    db.session.add(vet)
    db.session.commit()
    return jsonify({"mensagem": "Veterinário cadastrado", "id": vet.id}), 201

@app.route("/vets", methods=["GET"])
def listar_vets():
    """
    Listar todos os veterinários
    ---
    responses:
      200:
        description: Lista de veterinários
    """
    vets = Vet.query.all()
    return jsonify([v.to_dict() for v in vets])

@app.route("/vets/<int:id>", methods=["GET"])
def buscar_vet(id):
    """
    Buscar veterinário por ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Veterinário encontrado
      404:
        description: Veterinário não encontrado
    """
    vet = Vet.query.get(id)
    if vet:
        return jsonify(vet.to_dict())
    return jsonify({"erro": "Veterinário não encontrado"}), 404

@app.route("/vets/<int:id>", methods=["PUT"])
def atualizar_vet(id):
    """
    Atualizar veterinário
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        schema:
          $ref: '#/definitions/VetCreate'
    responses:
      200:
        description: Veterinário atualizado
      404:
        description: Veterinário não encontrado
    """
    vet = Vet.query.get(id)
    if not vet:
        return jsonify({"erro": "Veterinário não encontrado"}), 404
    dados = request.json
    schema = VetCreateSchema(**dados)
    for key, value in schema.dict().items():
        setattr(vet, key, value)
    db.session.commit()
    return jsonify({"mensagem": "Veterinário atualizado"})

@app.route("/vets/<int:id>", methods=["DELETE"])
def deletar_vet(id):
    """
    Deletar veterinário
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Veterinário deletado
      404:
        description: Veterinário não encontrado
    """
    vet = Vet.query.get(id)
    if not vet:
        return jsonify({"erro": "Veterinário não encontrado"}), 404
    db.session.delete(vet)
    db.session.commit()
    return jsonify({"mensagem": "Veterinário deletado"})

# ------------------------- 
# Rotas APPOINTMENTS
# -------------------------
@app.route("/appointments", methods=["POST"])
def criar_appointment():
    """
    Criar um novo agendamento
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/AppointmentCreate'
    responses:
      201:
        description: Agendamento criado
    """
    dados = request.json
    schema = AppointmentCreateSchema(**dados)
    appointment = Appointment(**schema.dict())
    db.session.add(appointment)
    db.session.commit()
    return jsonify({"mensagem": "Agendamento criado", "id": appointment.id}), 201

@app.route("/appointments", methods=["GET"])
def listar_appointments():
    """
    Listar todos os agendamentos
    ---
    responses:
      200:
        description: Lista de agendamentos
    """
    appointments = Appointment.query.all()
    return jsonify([a.to_dict() for a in appointments])

@app.route("/appointments/<int:id>", methods=["GET"])
def buscar_appointment(id):
    """
    Buscar agendamento por ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Agendamento encontrado
      404:
        description: Agendamento não encontrado
    """
    appointment = Appointment.query.get(id)
    if appointment:
        return jsonify(appointment.to_dict())
    return jsonify({"erro": "Agendamento não encontrado"}), 404

@app.route("/appointments/<int:id>", methods=["DELETE"])
def deletar_appointment(id):
    """
    Deletar agendamento
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Agendamento deletado
      404:
        description: Agendamento não encontrado
    """
    appointment = Appointment.query.get(id)
    if not appointment:
        return jsonify({"erro": "Agendamento não encontrado"}), 404
    db.session.delete(appointment)
    db.session.commit()
    return jsonify({"mensagem": "Agendamento deletado"})

# ------------------------- 
# External API Integration
# -------------------------
@app.route("/address/<cep>", methods=["GET"])
def buscar_endereco(cep):
    """
    Buscar endereço por CEP usando ViaCEP
    ---
    parameters:
      - name: cep
        in: path
        type: string
        required: true
    responses:
      200:
        description: Endereço encontrado
      404:
        description: CEP não encontrado
    """
    response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
    if response.status_code == 200:
        data = response.json()
        if 'erro' not in data:
            return jsonify(data)
    return jsonify({"erro": "CEP não encontrado"}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5001)
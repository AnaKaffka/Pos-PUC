from flask import Flask, request, jsonify
from flask_cors import CORS
from flasgger import Swagger
from model.db import db
from model.pet import Pet
from model.diario import Diario
from model.observacao import Observacao
from schemas.pet_schema import PetCreateSchema, PetResponseSchema
from schemas.diario_schema import DiarioCreateSchema, DiarioResponseSchema
from schemas.observacao_schema import ObservacaoCreateSchema, ObservacaoResponseSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
db.init_app(app)
swagger = Swagger(app)

with app.app_context():
    db.create_all()

# ------------------------- 
# Rotas PET
# -------------------------
@app.route("/pets", methods=["POST"])
def cadastrar_pet():
    """
    Cadastrar um novo pet
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/PetCreate'
    responses:
      201:
        description: Pet cadastrado
    """
    dados = request.json
    schema = PetCreateSchema(**dados)
    pet = Pet(**schema.dict())
    db.session.add(pet)
    db.session.commit()
    return jsonify({"mensagem": "Pet cadastrado", "id": pet.id}), 201

@app.route("/pets", methods=["GET"])
def listar_pets():
    """
    Listar todos os pets
    ---
    responses:
      200:
        description: Lista de pets
    """
    pets = Pet.query.all()
    return jsonify([p.to_dict() for p in pets])

@app.route("/pets/<int:id>", methods=["GET"])
def buscar_pet(id):
    """
    Buscar pet por ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Pet encontrado
      404:
        description: Pet não encontrado
    """
    pet = Pet.query.get(id)
    if pet:
        return jsonify(pet.to_dict())
    return jsonify({"erro": "Pet não encontrado"}), 404

@app.route("/pets/<int:id>", methods=["PUT"])
def atualizar_pet(id):
    """
    Atualizar foto do pet
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        schema:
          type: object
          properties:
            foto:
              type: string
    responses:
      200:
        description: Pet atualizado
      404:
        description: Pet não encontrado
    """
    pet = Pet.query.get(id)
    if not pet:
        return jsonify({"erro": "Pet não encontrado"}), 404
    dados = request.json
    if 'foto' in dados:
        pet.foto = dados['foto']
    db.session.commit()
    return jsonify({"mensagem": "Pet atualizado"})

@app.route("/pets/<int:id>", methods=["DELETE"])
def deletar_pet(id):
    """
    Deletar pet
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Pet deletado
      404:
        description: Pet não encontrado
    """
    pet = Pet.query.get(id)
    if not pet:
        return jsonify({"erro": "Pet não encontrado"}), 404
    db.session.delete(pet)
    db.session.commit()
    return jsonify({"mensagem": "Pet deletado"})

# ------------------------- 
# Rotas DIARIO
# -------------------------
@app.route("/diario/<int:pet_id>", methods=["GET"])
def buscar_diario(pet_id):
    """
    Buscar diário do pet
    ---
    parameters:
      - name: pet_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Diário encontrado
      404:
        description: Diário não encontrado
    """
    diario = Diario.query.filter_by(pet_id=pet_id).first()
    if diario:
        return jsonify(diario.to_dict())
    return jsonify({"erro": "Diário não encontrado"}), 404

@app.route("/diario/<int:pet_id>", methods=["POST"])
def criar_diario(pet_id):
    """
    Criar ou atualizar diário do pet
    ---
    parameters:
      - name: pet_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/DiarioCreate'
    responses:
      201:
        description: Diário criado
      200:
        description: Diário atualizado
    """
    dados = request.json
    schema = DiarioCreateSchema(**dados)
    diario = Diario.query.filter_by(pet_id=pet_id).first()
    if diario:
        for key, value in schema.dict().items():
            setattr(diario, key, value)
        db.session.commit()
        return jsonify({"mensagem": "Diário atualizado"})
    else:
        diario = Diario(pet_id=pet_id, **schema.dict())
        db.session.add(diario)
        db.session.commit()
        return jsonify({"mensagem": "Diário criado", "id": diario.id}), 201

# ------------------------- 
# Rotas OBSERVACOES
# -------------------------
@app.route("/observacoes/<int:pet_id>", methods=["POST"])
def adicionar_observacao(pet_id):
    """
    Adicionar observação ao pet
    ---
    parameters:
      - name: pet_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/ObservacaoCreate'
    responses:
      201:
        description: Observação adicionada
    """
    dados = request.json
    schema = ObservacaoCreateSchema(**dados)
    observacao = Observacao(pet_id=pet_id, **schema.dict())
    db.session.add(observacao)
    db.session.commit()
    return jsonify({"mensagem": "Observação adicionada", "id": observacao.id}), 201

@app.route("/observacoes/<int:pet_id>", methods=["GET"])
def listar_observacoes(pet_id):
    """
    Listar observações do pet
    ---
    parameters:
      - name: pet_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Lista de observações
    """
    observacoes = Observacao.query.filter_by(pet_id=pet_id).order_by(Observacao.data.desc()).all()
    return jsonify([o.to_dict() for o in observacoes])

if __name__ == "__main__":
    app.run(debug=True)
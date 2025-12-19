from flask import Flask, request, jsonify, send_from_directory
import sqlite3
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from model.db import criar_tabelas
from model.pet import Pet
from model.diario import Diario
from model.observacao import Observacao
from schemas.pet_schema import PetCreateSchema, PetResponseSchema
from schemas.diario_schema import DiarioCreateSchema, DiarioResponseSchema
from schemas.observacao_schema import ObservacaoCreateSchema

app = Flask(__name__)
CORS(app)

# -------------------------
# Banco de dados
# -------------------------
criar_tabelas()

# -------------------------
# Rotas PET
# -------------------------
@app.route("/pets", methods=["POST"])
def cadastrar_pet():
    dados = request.json
    schema = PetCreateSchema(**dados)
    result = Pet.cadastrar(schema.dict())
    return jsonify(result), 201


@app.route("/pets", methods=["GET"])
def listar_pets():
    pets = Pet.listar()
    return jsonify(pets)


@app.route("/pets/<int:id>", methods=["GET"])
def buscar_pet(id):
    pet = Pet.buscar(id)
    if pet:
        return jsonify(pet)
    return jsonify({"erro": "Pet não encontrado"}), 404


@app.route("/pets/<int:id>", methods=["PUT"])
def atualizar_foto_pet(id):
    dados = request.json
    # For update, we only need foto
    if "foto" not in dados:
        return jsonify({"erro": "Foto é obrigatória"}), 400
    result = Pet.atualizar_foto(id, dados["foto"])
    return jsonify(result)

@app.route("/pets/<int:id>", methods=["DELETE"])
def deletar_pet(id):
    try:
        result = Pet.deletar(id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# -------------------------
# Rotas DIÁRIO
# -------------------------
@app.route("/pets/<int:id>/diario", methods=["POST"])
def adicionar_diario(id):
    dados = request.json
    schema = DiarioCreateSchema(**dados)
    result = Diario.adicionar(id, schema.dict())
    return jsonify(result), 201


@app.route("/pets/<int:id>/diario", methods=["PUT"])
def atualizar_diario(id):
    dados = request.json
    schema = DiarioCreateSchema(**dados)
    result = Diario.atualizar(id, schema.dict())
    return jsonify(result)


@app.route("/pets/<int:id>/diario", methods=["GET"])
def listar_diario(id):
    # Retorna apenas um registro (o primeiro)
    diario = Diario.buscar_ou_criar(id)
    return jsonify(diario if diario else {})

# -------------------------
# Rotas OBSERVAÇÕES
# -------------------------
@app.route("/pets/<int:id>/observacoes", methods=["POST"])
def adicionar_observacao(id):
    dados = request.json
    schema = ObservacaoCreateSchema(**dados)
    result = Observacao.adicionar(id, schema.data, schema.texto)
    return jsonify(result), 201


@app.route("/pets/<int:id>/observacoes", methods=["GET"])
def listar_observacoes(id):
    observacoes = Observacao.listar(id)
    return jsonify(observacoes)


@app.route("/observacoes/<int:id>", methods=["DELETE"])
def deletar_observacao(id):
    try:
        result = Observacao.deletar(id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# -------------------------
# Swagger
# -------------------------
SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Diário de Pets API"}
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route("/")
def home():
    return send_from_directory('static', 'index.html')

@app.route("/api")
def api_home():
    return jsonify({"message": "API de Diário de Pets", "swagger": f"{request.host_url.rstrip('/')}/swagger"})

if __name__ == "__main__":
    app.run(debug=True)

import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import requests
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GeoDistance API",
    description="Cálculo de distância entre CEPs",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = SessionLocal()
VIACEP_URL = "https://viacep.com.br/ws"
SECONDARY_API_URL = os.getenv("SECONDARY_API_URL", "http://localhost:8001")
SECONDARY_API_TIMEOUT = float(os.getenv("SECONDARY_API_TIMEOUT", "30"))
SECONDARY_API_RETRIES = int(os.getenv("SECONDARY_API_RETRIES", "1"))

class DistanciaRequest(BaseModel):
    cep_origem: str = Field(..., example="22041001")
    cep_destino: str = Field(..., example="01311000")


def validar_cep(cep: str):
    return cep.isdigit() and len(cep) == 8


def consultar_api_secundaria(payload: dict):
    ultima_excecao = None
    for tentativa in range(SECONDARY_API_RETRIES + 1):
        try:
            return requests.post(
                f"{SECONDARY_API_URL}/calcular",
                json=payload,
                timeout=SECONDARY_API_TIMEOUT,
            )
        except requests.Timeout as exc:
            ultima_excecao = exc
            if tentativa < SECONDARY_API_RETRIES:
                continue
            raise HTTPException(
                504,
                f"Timeout ao consultar API secundaria apos {SECONDARY_API_TIMEOUT}s",
            )
        except requests.RequestException as exc:
            ultima_excecao = exc
            break

    raise HTTPException(502, f"Falha ao consultar a API secundaria: {ultima_excecao}")


@app.get("/cep/{cep}", tags=["CEP"])
def get_cep(cep: str):
    response = requests.get(f"{VIACEP_URL}/{cep}/json/")
    return response.json()


@app.post("/distancia", tags=["Distância"])
def calcular_distancia(data: DistanciaRequest):
    cep1 = data.cep_origem
    cep2 = data.cep_destino

    if not validar_cep(cep1) or not validar_cep(cep2):
        raise HTTPException(400, "CEP inválido")

    endereco1 = requests.get(f"{VIACEP_URL}/{cep1}/json/", timeout=10).json()
    endereco2 = requests.get(f"{VIACEP_URL}/{cep2}/json/", timeout=10).json()

    if endereco1.get("erro") or endereco2.get("erro"):
        raise HTTPException(404, "CEP não encontrado")

    response = consultar_api_secundaria({"cep1": cep1, "cep2": cep2})

    if not response.ok:
        detalhe = "Falha ao consultar a API secundária"
        try:
            detalhe = response.json().get("detail", detalhe)
        except ValueError:
            pass
        raise HTTPException(response.status_code, detalhe)

    distancia = response.json().get("distancia")
    if not distancia:
        raise HTTPException(502, "Resposta inválida da API secundária")

    registro = models.Historico(
        cep_origem=cep1,
        cep_destino=cep2,
        distancia=distancia
    )
    db.add(registro)
    db.commit()

    return {
        "id": registro.id,
        "distancia": distancia,
        "origem": endereco1,
        "destino": endereco2
    }


@app.get("/historico", tags=["Histórico"])
def listar_historico():
    registros = db.query(models.Historico).order_by(models.Historico.id.desc()).all()
    return [
        {"id": r.id, "cep_origem": r.cep_origem, "cep_destino": r.cep_destino, "distancia": r.distancia}
        for r in registros
    ]


@app.put("/historico/{id}", tags=["Histórico"])
def atualizar(id: int, data: dict):
    registro = db.query(models.Historico).get(id)
    if not registro:
        raise HTTPException(404, "Registro não encontrado")
    registro.distancia = data.get("distancia")
    db.commit()
    return {"msg": "Atualizado"}


@app.delete("/historico/{id}", tags=["Histórico"])
def deletar(id: int):
    registro = db.query(models.Historico).get(id)
    if not registro:
        raise HTTPException(404, "Registro não encontrado")
    db.delete(registro)
    db.commit()
    return {"msg": "Deletado"}
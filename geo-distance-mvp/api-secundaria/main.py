from functools import lru_cache
from math import radians, cos, sin, asin, sqrt

import requests
from fastapi import FastAPI, HTTPException

app = FastAPI()
VIACEP_URL = "https://viacep.com.br/ws"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

def haversine(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return 6371 * c


def buscar_nominatim(params: dict):
    resposta = requests.get(
        NOMINATIM_URL,
        params={**params, "format": "jsonv2", "limit": 1, "countrycodes": "br"},
        headers={"User-Agent": "geo-distance-mvp/1.0"},
        timeout=10,
    )
    if not resposta.ok:
        raise HTTPException(502, "Falha ao consultar o servico de geocodificacao")
    return resposta.json()


@lru_cache(maxsize=256)
def buscar_coordenadas_por_cep(cep: str):
    endereco = requests.get(f"{VIACEP_URL}/{cep}/json/", timeout=10).json()
    if endereco.get("erro"):
        raise HTTPException(404, f"CEP {cep} nao encontrado")

    consultas = []

    if endereco.get("logradouro") and endereco.get("bairro"):
        consultas.append(
            {
                "q": ", ".join(
                    parte
                    for parte in [
                        endereco.get("logradouro"),
                        endereco.get("bairro"),
                        endereco.get("localidade"),
                        endereco.get("uf"),
                        cep,
                        "Brasil",
                    ]
                    if parte
                )
            }
        )

    if endereco.get("logradouro"):
        consultas.append(
            {
                "street": endereco["logradouro"],
                "city": endereco.get("localidade", ""),
                "state": endereco.get("uf", ""),
                "postalcode": cep,
            }
        )
        consultas.append(
            {
                "q": ", ".join(
                    parte
                    for parte in [
                        endereco.get("logradouro"),
                        endereco.get("localidade"),
                        endereco.get("uf"),
                        "Brasil",
                    ]
                    if parte
                )
            }
        )

    if endereco.get("bairro"):
        consultas.append(
            {
                "q": ", ".join(
                    parte
                    for parte in [
                        endereco.get("bairro"),
                        endereco.get("localidade"),
                        endereco.get("uf"),
                        "Brasil",
                    ]
                    if parte
                )
            }
        )

    consultas.extend(
        [
            {"q": ", ".join(parte for parte in [cep, endereco.get("localidade"), endereco.get("uf"), "Brasil"] if parte)},
            {"postalcode": cep, "city": endereco.get("localidade", ""), "state": endereco.get("uf", "")},
            {"q": ", ".join(parte for parte in [endereco.get("localidade"), endereco.get("uf"), "Brasil"] if parte)},
        ]
    )

    dados = []
    for params in consultas:
        dados = buscar_nominatim(params)
        if dados:
            break

    if not dados:
        raise HTTPException(404, f"Nao foi possivel localizar coordenadas para o CEP {cep}")

    return float(dados[0]["lat"]), float(dados[0]["lon"])


@app.post("/calcular")
def calcular(data: dict):
    cep1 = data.get("cep1")
    cep2 = data.get("cep2")
    if not cep1 or not cep2:
        raise HTTPException(400, "cep1 e cep2 sao obrigatorios")

    lat1, lon1 = buscar_coordenadas_por_cep(cep1)
    lat2, lon2 = buscar_coordenadas_por_cep(cep2)

    if cep1 != cep2 and abs(lat1 - lat2) < 1e-7 and abs(lon1 - lon2) < 1e-7:
        raise HTTPException(422, "Nao foi possivel obter coordenadas distintas para os CEPs informados")

    distancia = haversine(lat1, lon1, lat2, lon2)

    return {"distancia": f"{round(distancia, 2)} km"}
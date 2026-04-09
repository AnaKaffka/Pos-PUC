from functools import lru_cache
from math import radians, cos, sin, asin, sqrt
from typing import Dict

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="GeoDistance Secondary API",
    description="Geocodificação e cálculo de distância por estrada entre CEPs",
    version="1.0.0",
)

VIACEP_URL = "https://viacep.com.br/ws"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
BRASILAPI_URL = "https://brasilapi.com.br/api/cep/v2"

# Servidores OSRM tentados em ordem; o primeiro que responder é usado
OSRM_SERVERS = [
    "http://router.project-osrm.org/route/v1/driving",
    "https://routing.openstreetmap.de/routed-car/route/v1/driving",
]

# Overrides manuais de coordenadas (persistidos em memória)
_coordenadas_override: Dict[str, tuple] = {}


class CalcularRequest(BaseModel):
    cep1: str
    cep2: str


class CoordenadasRequest(BaseModel):
    lat: float
    lon: float

def haversine(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return 6371 * c


def buscar_coordenadas_brasilapi(cep: str):
    """Obtém coordenadas direto da BrasilAPI v2 (mais precisa para CEPs brasileiros)."""
    try:
        r = requests.get(
            f"{BRASILAPI_URL}/{cep}",
            headers={"User-Agent": "geo-distance-mvp/1.0"},
            timeout=8,
        )
        if not r.ok:
            return None
        data = r.json()
        coords = (data.get("location") or {}).get("coordinates") or {}
        lat = coords.get("latitude")
        lon = coords.get("longitude")
        if lat and lon:
            return float(lat), float(lon)
    except Exception:
        pass
    return None


def calcular_distancia_rota(lat1: float, lon1: float, lat2: float, lon2: float):
    """Tenta calcular distância por estrada em dois servidores OSRM.
    Retorna (distancia_km, servidor_usado) ou (None, None) se todos falharem."""
    for base_url in OSRM_SERVERS:
        try:
            url = f"{base_url}/{lon1},{lat1};{lon2},{lat2}"
            r = requests.get(
                url,
                params={"overview": "false"},
                headers={"User-Agent": "geo-distance-mvp/1.0"},
                timeout=15,
            )
            if r.ok:
                data = r.json()
                if data.get("routes"):
                    return data["routes"][0]["distance"] / 1000, base_url
        except Exception:
            continue
    return None, None


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
    # Tenta BrasilAPI primeiro: coordenadas diretas e mais precisas para CEPs BR
    resultado = buscar_coordenadas_brasilapi(cep)
    if resultado:
        return resultado

    # Fallback: ViaCEP + Nominatim
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


def _obter_coordenadas(cep: str):
    """Retorna coordenadas, priorizando override manual."""
    if cep in _coordenadas_override:
        return _coordenadas_override[cep]
    return buscar_coordenadas_por_cep(cep)


@app.get("/coordenadas/{cep}", tags=["Coordenadas"])
def obter_coordenadas(cep: str):
    """Retorna as coordenadas (lat/lon) de um CEP."""
    if not cep.isdigit() or len(cep) != 8:
        raise HTTPException(400, "CEP invalido: deve conter exatamente 8 digitos")
    lat, lon = _obter_coordenadas(cep)
    return {"cep": cep, "lat": lat, "lon": lon}


@app.put("/coordenadas/{cep}", tags=["Coordenadas"])
def definir_coordenadas(cep: str, dados: CoordenadasRequest):
    """Define manualmente as coordenadas de um CEP (override)."""
    if not cep.isdigit() or len(cep) != 8:
        raise HTTPException(400, "CEP invalido: deve conter exatamente 8 digitos")
    _coordenadas_override[cep] = (dados.lat, dados.lon)
    buscar_coordenadas_por_cep.cache_clear()
    return {"msg": "Coordenadas definidas manualmente", "cep": cep, "lat": dados.lat, "lon": dados.lon}


@app.delete("/coordenadas/{cep}", tags=["Coordenadas"])
def remover_coordenadas(cep: str):
    """Remove o override manual de coordenadas de um CEP."""
    if cep not in _coordenadas_override:
        raise HTTPException(404, "Nenhum override de coordenada encontrado para este CEP")
    del _coordenadas_override[cep]
    buscar_coordenadas_por_cep.cache_clear()
    return {"msg": "Override removido", "cep": cep}


@app.post("/calcular", tags=["Distância"])
def calcular(data: CalcularRequest):
    """Calcula a distância em km entre dois CEPs."""
    cep1 = data.cep1
    cep2 = data.cep2

    lat1, lon1 = _obter_coordenadas(cep1)
    lat2, lon2 = _obter_coordenadas(cep2)

    if cep1 != cep2 and abs(lat1 - lat2) < 1e-7 and abs(lon1 - lon2) < 1e-7:
        raise HTTPException(422, "Nao foi possivel obter coordenadas distintas para os CEPs informados")

    distancia, servidor = calcular_distancia_rota(lat1, lon1, lat2, lon2)
    if distancia is not None:
        return {
            "distancia": f"{round(distancia, 2)} km",
            "metodo": "estrada",
            "servidor": servidor,
        }

    # Fallback: Haversine (linha reta)
    distancia = haversine(lat1, lon1, lat2, lon2)
    return {
        "distancia": f"{round(distancia, 2)} km",
        "metodo": "linha_reta (roteamento indisponivel)",
        "servidor": None,
    }


@app.get("/debug/{cep1}/{cep2}", tags=["Debug"])
def debug_distancia(cep1: str, cep2: str):
    """Diagnóstico: mostra coordenadas usadas e resposta bruta do roteamento."""
    lat1, lon1 = _obter_coordenadas(cep1)
    lat2, lon2 = _obter_coordenadas(cep2)
    detalhes = {
        "cep1": {"cep": cep1, "lat": lat1, "lon": lon1},
        "cep2": {"cep": cep2, "lat": lat2, "lon": lon2},
        "haversine_km": round(haversine(lat1, lon1, lat2, lon2), 2),
        "osrm_tentativas": [],
    }
    for base_url in OSRM_SERVERS:
        entrada = {"servidor": base_url}
        try:
            url = f"{base_url}/{lon1},{lat1};{lon2},{lat2}"
            r = requests.get(url, params={"overview": "false"}, timeout=15)
            entrada["status"] = r.status_code
            if r.ok and r.json().get("routes"):
                entrada["distancia_km"] = round(r.json()["routes"][0]["distance"] / 1000, 2)
            else:
                entrada["erro"] = r.text[:200]
        except Exception as e:
            entrada["erro"] = str(e)
        detalhes["osrm_tentativas"].append(entrada)
    return detalhes
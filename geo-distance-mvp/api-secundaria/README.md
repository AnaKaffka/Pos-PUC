# GeoDistance — API Secundária

API REST construída com **FastAPI** responsável por geocodificar CEPs brasileiros e calcular a distância em linha reta entre dois pontos usando a fórmula de **Haversine**.

Ela é chamada exclusivamente pela API Principal e não deve ser exposta diretamente ao usuário final.

---

## Tecnologias

| Tecnologia | Função |
|---|---|
| Python 3.11 | Linguagem |
| FastAPI | Framework web |
| Uvicorn | Servidor ASGI |
| Requests | Chamadas HTTP externas |
| [ViaCEP](https://viacep.com.br) | Resolução de endereço a partir do CEP |
| [Nominatim / OpenStreetMap](https://nominatim.openstreetmap.org) | Geocodificação (endereço → coordenadas) |

---

## Estrutura

```
api-secundaria/
├── main.py          # Lógica de geocodificação e cálculo
├── requirements.txt
└── Dockerfile
```

---

## Como funciona

```
cep1, cep2
    │
    ▼
ViaCEP  ──►  endereço completo (logradouro, bairro, cidade, UF)
    │
    ▼
Nominatim  ──►  latitude / longitude
    │
    ▼
Haversine  ──►  distância em km
```

### Estratégia de geocodificação

Para cada CEP, a API tenta as seguintes consultas ao Nominatim em ordem de especificidade, parando na primeira que retornar resultado:

1. Logradouro + bairro + cidade + UF + CEP
2. Logradouro (campo estruturado) + cidade + UF + CEP
3. Logradouro + cidade + UF
4. Bairro + cidade + UF
5. CEP + cidade + UF
6. CEP (campo `postalcode`) + cidade + UF
7. Cidade + UF (fallback mínimo)

Se dois CEPs diferentes resultarem em coordenadas idênticas (falso centróide), a API retorna erro `422` em vez de devolver `0.0 km`.

### Fórmula de Haversine

$$d = 2r \arcsin\!\left(\sqrt{\sin^2\!\frac{\Delta\phi}{2} + \cos\phi_1\cos\phi_2\sin^2\!\frac{\Delta\lambda}{2}}\right)$$

Onde $r = 6371$ km (raio médio da Terra), $\phi$ = latitude e $\lambda$ = longitude em radianos.

> O resultado é a **distância em linha reta** (geodésica), não o tempo de trajeto viário.

---

## Endpoint

### `POST /calcular`

Recebe dois CEPs e retorna a distância calculada.

**Body:**
```json
{
  "cep1": "71060901",
  "cep2": "70342040"
}
```

**Resposta 200:**
```json
{
  "distancia": "4.93 km"
}
```

**Erros possíveis:**

| Código | Motivo |
|---|---|
| 400 | `cep1` ou `cep2` ausente no body |
| 404 | CEP não encontrado no ViaCEP ou sem coordenadas no Nominatim |
| 422 | CEPs diferentes mas com coordenadas idênticas (centróide genérico) |
| 502 | Falha na comunicação com o Nominatim |

---

## Cache

As coordenadas geocodificadas ficam em memória via `@lru_cache(maxsize=256)`. CEPs já consultados não fazem novas chamadas externas durante a vida do processo.

---

## Como rodar

### Com Docker Compose (recomendado)

Na raiz do repositório `geo-distance-mvp/`:

```bash
docker compose up --build
```

A API ficará disponível em `http://localhost:8001`.

### Localmente (sem Docker)

```bash
cd api-secundaria
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

Documentação interativa: `http://localhost:8001/docs`

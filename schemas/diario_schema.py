from pydantic import BaseModel

class DiarioCreateSchema(BaseModel):
    comida_preferida: str
    veterinario: str
    data_vacinacao: str
    peso: float
    observacoes: str

class DiarioResponseSchema(BaseModel):
    id: int
    comida_preferida: str
    veterinario: str
    data_vacinacao: str
    peso: float
    observacoes: str
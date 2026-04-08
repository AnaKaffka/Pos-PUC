from pydantic import BaseModel
from typing import Optional

class DiarioCreateSchema(BaseModel):
    comida_preferida: Optional[str] = ""
    veterinario: Optional[str] = ""
    data_vacinacao: Optional[str] = ""
    peso: Optional[float] = 0.0
    observacoes: Optional[str] = ""

class DiarioResponseSchema(BaseModel):
    id: int
    comida_preferida: str
    veterinario: str
    data_vacinacao: str
    peso: float
    observacoes: str
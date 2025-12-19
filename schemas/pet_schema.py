from pydantic import BaseModel

class PetCreateSchema(BaseModel):
    nome: str
    idade: int
    tipo: str

class PetResponseSchema(BaseModel):
    id: int
    nome: str
    idade: int
    tipo: str
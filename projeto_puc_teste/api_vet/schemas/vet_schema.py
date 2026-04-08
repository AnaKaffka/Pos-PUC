from pydantic import BaseModel

class VetCreateSchema(BaseModel):
    nome: str
    especialidade: str = None
    endereco: str = None
    telefone: str = None

class VetResponseSchema(BaseModel):
    id: int
    nome: str
    especialidade: str = None
    endereco: str = None
    telefone: str = None
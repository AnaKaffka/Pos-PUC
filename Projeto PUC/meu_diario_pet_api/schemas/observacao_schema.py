from pydantic import BaseModel

class ObservacaoCreateSchema(BaseModel):
    data: str
    texto: str

class ObservacaoResponseSchema(BaseModel):
    id: int
    data: str
    texto: str

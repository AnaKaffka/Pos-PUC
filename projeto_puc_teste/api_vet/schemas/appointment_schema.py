from pydantic import BaseModel

class AppointmentCreateSchema(BaseModel):
    pet_id: int
    vet_id: int
    data: str
    motivo: str = None

class AppointmentResponseSchema(BaseModel):
    id: int
    pet_id: int
    vet_id: int
    data: str
    motivo: str = None
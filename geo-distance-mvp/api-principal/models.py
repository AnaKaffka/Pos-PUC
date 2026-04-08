from sqlalchemy import Column, Integer, String
from database import Base

class Historico(Base):
    __tablename__ = "historico"

    id = Column(Integer, primary_key=True)
    cep_origem = Column(String)
    cep_destino = Column(String)
    distancia = Column(String)
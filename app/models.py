from pydantic import BaseModel, Field
from typing import Optional
import uuid

class PedidoBase(BaseModel):
    nome_cliente: str
    nome_produto: str
    quantidade: int

class PedidoCreate(PedidoBase):
    pass

class PedidoResponse(PedidoBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: str = "PENDENTE"

    class Config:
        populate_by_name = True
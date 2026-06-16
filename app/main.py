from fastapi import FastAPI, status
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from contextlib import asynccontextmanager

from app.config import settings
from app.database import db_instance, get_database
from app.models import PedidoCreate, PedidoResponse
from app.brokers.rabbit import publish_to_rabbitmq
from app.brokers.kafka_producer import publish_to_kafka

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_instance.client = AsyncIOMotorClient(settings.MONGO_URI)
    db_instance.db = db_instance.client[settings.MONGO_DB]
    yield
    db_instance.client.close()

app = FastAPI(title="API de Gerenciamento de Pedidos", lifespan=lifespan)

@app.post("/pedidos", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
async def criar_pedido(pedido: PedidoCreate):
    db = get_database()
    
    novo_pedido = PedidoResponse(**pedido.model_dump())
    pedido_dict = novo_pedido.model_dump()
    
    await db["pedidos"].insert_one(pedido_dict)
    
    msg_rabbit = {"id": novo_pedido.id, "status": novo_pedido.status}
    await publish_to_rabbitmq(msg_rabbit)
    
    msg_kafka = {
        "event": "PEDIDO_CRIADO",
        "data": pedido_dict
    }
    await publish_to_kafka(msg_kafka)
    
    return novo_pedido

@app.get("/pedidos", response_model=List[PedidoResponse])
async def listar_pedidos():
    db = get_database()
    cursor = db["pedidos"].find()
    pedidos = await cursor.to_list(length=100)
    return pedidos
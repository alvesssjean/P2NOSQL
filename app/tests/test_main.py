import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from motor.motor_asyncio import AsyncIOMotorClient

from app.main import app
from app.config import settings
from app.database import db_instance

@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    db_instance.client = AsyncIOMotorClient(settings.MONGO_URI)
    db_instance.db = db_instance.client[settings.MONGO_DB]
    yield
    await db_instance.db["pedidos"].drop()
    db_instance.client.close()

@pytest.mark.asyncio
@patch("app.main.publish_to_rabbitmq", new_callable=AsyncMock)
@patch("app.main.publish_to_kafka", new_callable=AsyncMock)
async def test_criar_e_listar_pedido(mock_kafka, mock_rabbit):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        
        payload = {
            "nome_cliente": "Fulano Ciclano",
            "nome_produto": "Teclado Mecânico",
            "quantidade": 1
        }
        response = await ac.post("/pedidos", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["nome_cliente"] == payload["nome_cliente"]
        assert data["status"] == "PENDENTE"
        assert "id" in data
        
        mock_rabbit.assert_called_once()
        mock_kafka.assert_called_once()

        response_list = await ac.get("/pedidos")
        assert response_list.status_code == 200
        assert len(response_list.json()) > 0
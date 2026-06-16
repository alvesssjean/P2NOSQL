import json
import aio_pika
from app.config import settings

async def publish_to_rabbitmq(message: dict):
    try:
        connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        async with connection:
            channel = await connection.channel()
            await channel.declare_queue(settings.RABBITMQ_QUEUE, durable=True)
            
            await channel.default_exchange.publish(
                aio_pika.Message(body=json.dumps(message).encode()),
                routing_key=settings.RABBITMQ_QUEUE,
            )
    except Exception as e:
        print(f"Erro ao publicar no RabbitMQ: {e}")
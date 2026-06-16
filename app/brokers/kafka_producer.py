import json
from aiokafka import AIOKafkaProducer
from app.config import settings

async def publish_to_kafka(message: dict):
    try:
        producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)
        await producer.start()
        try:
            payload = json.dumps(message).encode('utf-8')
            await producer.send_and_wait(settings.KAFKA_TOPIC, payload)
        finally:
            await producer.stop()
    except Exception as e:
        print(f"Erro ao publicar no Kafka: {e}")
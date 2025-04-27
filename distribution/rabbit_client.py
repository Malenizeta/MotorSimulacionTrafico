import aio_pika
import asyncio
import json

class RabbitClient:
    def __init__(self, amqp_url="amqp://guest:guest@localhost/"):
        self.amqp_url = amqp_url
        self.connection = None
        self.channel = None
        self.exchange = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.amqp_url)
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange('vehicles', aio_pika.ExchangeType.FANOUT)

    async def send_vehicle(self, vehicle_data: dict):
        if not self.exchange:
            raise Exception("RabbitMQ exchange not connected yet")

        message = aio_pika.Message(
            body=json.dumps(vehicle_data).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        await self.exchange.publish(message, routing_key="")

    async def consume_vehicles(self, callback):
        queue = await self.channel.declare_queue('', exclusive=True)
        await queue.bind(self.exchange)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    vehicle_data = json.loads(message.body)
                    await callback(vehicle_data)

    async def close(self):
        await self.connection.close()

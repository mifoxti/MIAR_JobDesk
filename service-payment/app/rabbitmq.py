import json
import traceback
from asyncio import AbstractEventLoop
from aio_pika.abc import AbstractRobustConnection
from aio_pika import connect_robust, IncomingMessage

from app.settings import settings


async def process_payment_notification(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        # TODO: Обработать сообщение о платеже
        print(f"Received payment notification: {data}")
        await msg.ack()
    except Exception as e:
        traceback.print_exc()
        await msg.ack()


async def consume(loop: AbstractEventLoop) -> AbstractRobustConnection:
    connection = await connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    queue = await channel.declare_queue('payment_notifications', durable=True)

    await queue.consume(process_payment_notification)
    print('Started RabbitMQ consuming for payments...')

    return connection

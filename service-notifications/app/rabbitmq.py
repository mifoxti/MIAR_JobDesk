import json
import traceback
from asyncio import AbstractEventLoop
from aio_pika.abc import AbstractRobustConnection
from aio_pika import connect_robust, IncomingMessage

from app.settings import settings
from app.services.notification_service import NotificationService


async def process_notification_request(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        service = NotificationService()
        # Example: depending on data, call appropriate method
        # For now, assume data has 'type' and params
        if data['type'] == 'new_message':
            notification = service.send_new_message_notification(data['recipient_id'], data['sender_name'])
        # etc for other types
        print(f"Processed notification: {data}")
        await msg.ack()
    except Exception as e:
        traceback.print_exc()
        await msg.ack()


async def consume(loop: AbstractEventLoop) -> AbstractRobustConnection:
    connection = await connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    queue = await channel.declare_queue('notification_requests', durable=True)

    await queue.consume(process_notification_request)
    print('Started RabbitMQ consuming for notifications...')

    return connection

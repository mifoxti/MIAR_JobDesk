import asyncio
from fastapi import FastAPI

from app import rabbitmq
from app.endpoints.notification_router import notification_router

app = FastAPI(title='Notification Service')

@app.on_event('startup')
def startup():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(rabbitmq.consume(loop))

app.include_router(notification_router, prefix='/api')

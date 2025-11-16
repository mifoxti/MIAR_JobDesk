import asyncio
from fastapi import FastAPI

from app import rabbitmq
from app.database import create_tables
from app.endpoints.payment_router import payment_router

app = FastAPI(title='Payment Service')

@app.on_event('startup')
def startup():
    # Создать таблицы в БД перед запуском
    create_tables()
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(rabbitmq.consume(loop))

app.include_router(payment_router, prefix='/api')

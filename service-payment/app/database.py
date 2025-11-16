from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.schemas.payment import Base
from app.schemas.task import Base as BaseTask

from app.settings import settings

engine = create_engine(settings.postgres_url, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Убрали create_all отсюда, сделаем в startup

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Функция создания таблиц в startup
def create_tables():
    Base.metadata.create_all(bind=engine)
    BaseTask.metadata.create_all(bind=engine)

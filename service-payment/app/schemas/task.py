from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base(name="BaseTask")

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    customer_id = Column(INTEGER, nullable=False)  # Заказчик

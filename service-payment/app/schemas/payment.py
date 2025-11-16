from sqlalchemy import Column, String, Float, DateTime, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

from app.models.payment import PaymentStatus, PaymentMethod

Base = declarative_base()

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_user_id = Column(Integer, nullable=False)  # Заказчик
    assigned_user_id = Column(Integer, nullable=False)  # Исполнитель
    task_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    created_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    transaction_id = Column(String, nullable=True)

    # Note: Balance checking would require user table in this DB or API call
    # For now, keep as is, balance is simulated

from enum import Enum
from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from typing import Optional


class PaymentStatus(str, Enum):
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'


class PaymentMethod(str, Enum):
    CARD = 'card'
    BANK_TRANSFER = 'bank_transfer'
    ELECTRONIC_WALLET = 'electronic_wallet'
    CRYPTO = 'crypto'


class Payment(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    customer_user_id: int  # Заказчик (из задачи)
    assigned_user_id: int  # Исполнитель (платит заказчик исполнителю)
    task_id: int
    amount: float
    payment_method: PaymentMethod
    status: PaymentStatus = PaymentStatus.PENDING
    created_at: Optional[str] = None
    completed_at: Optional[str] = None
    transaction_id: Optional[str] = None

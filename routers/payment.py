"""
Роутеры для работы с оплатой
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

router = APIRouter(prefix="/payment", tags=["payment"])


# Модели запросов
class PaymentMethodRequest(BaseModel):
    """Запрос на выбор способа оплаты"""
    task_id: int
    user_id: int
    amount: float
    payment_method: str  # card, bank_transfer, electronic_wallet, crypto


class ProcessPaymentRequest(BaseModel):
    """Запрос на выполнение оплаты"""
    payment_id: int
    payment_details: Optional[dict] = None  # Дополнительные детали для разных способов оплаты


# Модели ответов
class PaymentMethodResponse(BaseModel):
    """Ответ при выборе способа оплаты"""
    payment_id: int
    task_id: int
    user_id: int
    amount: float
    payment_method: str
    status: str
    message: str
    created_at: str


class ProcessPaymentResponse(BaseModel):
    """Ответ при выполнении оплаты"""
    payment_id: int
    status: str
    transaction_id: Optional[str] = None
    message: str
    completed_at: Optional[str] = None


# Временное хранилище платежей (в реальном приложении это должно быть в БД)
_payments_storage = {}
_payment_counter = 0


@router.post("/select-method", response_model=PaymentMethodResponse)
def select_payment_method(request: PaymentMethodRequest):
    """
    Выбрать способ оплаты для задачи
    
    Args:
        request: Данные о платеже (task_id, user_id, amount, payment_method)
        
    Returns:
        Информация о созданном платеже
    """
    global _payment_counter
    
    # Валидация способа оплаты
    valid_methods = ['card', 'bank_transfer', 'electronic_wallet', 'crypto']
    if request.payment_method not in valid_methods:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid payment method. Must be one of: {', '.join(valid_methods)}"
        )
    
    # Валидация суммы
    if request.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amount must be greater than 0"
        )
    
    # Создаем платеж
    _payment_counter += 1
    payment_id = _payment_counter
    
    payment_data = {
        "payment_id": payment_id,
        "task_id": request.task_id,
        "user_id": request.user_id,
        "amount": request.amount,
        "payment_method": request.payment_method,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "completed_at": None,
        "transaction_id": None
    }
    
    _payments_storage[payment_id] = payment_data
    
    return PaymentMethodResponse(
        payment_id=payment_id,
        task_id=request.task_id,
        user_id=request.user_id,
        amount=request.amount,
        payment_method=request.payment_method,
        status="pending",
        message=f"Payment method '{request.payment_method}' selected. Ready to process.",
        created_at=payment_data["created_at"]
    )


@router.post("/process", response_model=ProcessPaymentResponse)
def process_payment(request: ProcessPaymentRequest):
    """
    Произвести оплату
    
    Args:
        request: Данные о платеже (payment_id, payment_details)
        
    Returns:
        Результат выполнения оплаты
    """
    # Проверяем, существует ли платеж
    if request.payment_id not in _payments_storage:
        raise HTTPException(
            status_code=404,
            detail=f"Payment with id {request.payment_id} not found"
        )
    
    payment = _payments_storage[request.payment_id]
    
    # Проверяем статус платежа
    if payment["status"] != "pending":
        raise HTTPException(
            status_code=400,
            detail=f"Payment is already {payment['status']}. Cannot process again."
        )
    
    # Имитация обработки платежа
    import random
    import time
    
    # Устанавливаем статус "processing"
    payment["status"] = "processing"
    
    # Имитация задержки обработки
    time.sleep(0.1)
    
    # Имитация успешной/неуспешной оплаты (90% успех)
    is_successful = random.random() > 0.1
    
    if is_successful:
        payment["status"] = "completed"
        payment["transaction_id"] = f"TXN-{random.randint(100000, 999999)}"
        payment["completed_at"] = datetime.now().isoformat()
        message = f"Payment processed successfully. Transaction ID: {payment['transaction_id']}"
    else:
        payment["status"] = "failed"
        payment["completed_at"] = datetime.now().isoformat()
        message = "Payment processing failed. Please try again or contact support."
    
    return ProcessPaymentResponse(
        payment_id=request.payment_id,
        status=payment["status"],
        transaction_id=payment.get("transaction_id"),
        message=message,
        completed_at=payment.get("completed_at")
    )


@router.get("/{payment_id}", response_model=dict)
def get_payment(payment_id: int):
    """
    Получить информацию о платеже
    
    Args:
        payment_id: ID платежа
        
    Returns:
        Информация о платеже
    """
    if payment_id not in _payments_storage:
        raise HTTPException(
            status_code=404,
            detail=f"Payment with id {payment_id} not found"
        )
    
    return _payments_storage[payment_id]


@router.get("/", response_model=List[dict])
def get_all_payments():
    """
    Получить список всех платежей
    
    Returns:
        Список всех платежей
    """
    return list(_payments_storage.values())


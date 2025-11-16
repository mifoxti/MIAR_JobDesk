from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, List

from app.services.payment_service import PaymentService
from app.models.payment import Payment, PaymentMethod
from app.models.task import Task
from app.models.user import User
from app.repositories.task_repo import TaskRepo
from typing import List


payment_router = APIRouter(prefix='/payment', tags=['Payment'])


@payment_router.post("/select-method", response_model=Payment, summary="Выбрать способ оплаты для задачи")
def select_payment_method(
    task_id: int,
    assigned_user_id: int,
    payment_method: PaymentMethod,
    service: PaymentService = Depends()
):
    """
    Выбирает метод оплаты для задачи. Сумма берется из цены задачи, проверяется баланс заказчика.

    - **task_id**: ID задачи, которую нужно оплатить
    - **assigned_user_id**: ID исполнителя, которому переведут деньги
    - **payment_method**: Способ оплаты (card, bank_transfer, electronic_wallet, crypto)
    """
    try:
        return service.select_payment_method(task_id, assigned_user_id, payment_method)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@payment_router.post("/process", response_model=Payment, summary="Выполнить оплату")
def process_payment(
    payment_id: int,
    service: PaymentService = Depends()
):
    """
    Выполняет обработку платежа с имитацией успешности/неудачи.

    - **payment_id**: ID платежа из метода select-method

    Возможные статусы после обработки: COMPLETED, FAILED, с соответствующей датой и транзакцией.
    """
    try:
        return service.process_payment(payment_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Payment {payment_id} not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@payment_router.get("/{payment_id}", response_model=Payment, summary="Получить информацию о платеже")
def get_payment(
    payment_id: int,
    service: PaymentService = Depends()
):
    """
    Возвращает детальную информацию о конкретном платеже.

    - **payment_id**: ID платежа
    """
    try:
        return service.get_payment(payment_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Payment {payment_id} not found")


@payment_router.get("/", response_model=List[Payment], summary="Получить список всех платежей")
def get_all_payments(service: PaymentService = Depends()):
    """
    Возвращает список всех платежей в системе (для администраторов).
    """
    return service.get_all_payments()


@payment_router.get("/users/{user_id}/balance", summary="Получить баланс пользователя")
def get_user_balance(user_id: int, service: PaymentService = Depends()):
    """
    Возвращает текущий баланс пользователя (имитация для тестирования).

    - **user_id**: ID пользователя
    """
    balance = service.repo.check_balance(user_id)
    return {"user_id": user_id, "balance": balance}


@payment_router.get("/users/balances", summary="[TEST] Получить все балансы пользователей")
def get_all_user_balances():
    """
    Возвращает текущие балансы всех пользователей (для проверки изменений).
    """
    repo = TaskRepo()
    balances = repo.get_all_balances()
    return {"balances": balances}


# Test endpoints
@payment_router.get("/test/users", response_model=List[User], summary="[TEST] Получить всех тестовых пользователей")
def get_test_users():
    """
    Возвращает список тестовых пользователей с их актуальными балансами.
    """
    repo = TaskRepo()
    balances = repo.get_all_balances()

    # Создаем пользователей с реальными балансами
    users = []
    names = {
        1: ("Иван", "Иванов"),
        2: ("Петр", "Петров"),
        3: ("Мария", "Сидорова"),
        4: ("Алексей", "Васильев"),
        5: ("Ольга", "Николаева")
    }

    for user_id in balances:
        first_name, last_name = names.get(user_id, (f"User{user_id}", ""))
        users.append(User(id=user_id, first_name=first_name, last_name=last_name, balance=balances[user_id]))

    return users


@payment_router.get("/test/tasks", response_model=List[Task], summary="[TEST] Получить все тестовые задачи")
def get_test_tasks():
    """
    Возвращает список всех заданий из базы данных для оплаты.
    """
    repo = TaskRepo()
    return repo.get_all_tasks()


@payment_router.post("/test/create-task", response_model=Task, summary="[TEST] Создать тестовую задачу")
def create_test_task(title: str, description: str, price: float, customer_id: int):
    """
    Создает тестовую задачу и сохраняет в базе данных для оплаты.

    - **title**: Название задачи
    - **description**: Описание задачи
    - **price**: Стоимость задачи
    - **customer_id**: ID заказчика
    """
    task = Task(title=title, description=description, price=price, customer_id=customer_id)
    repo = TaskRepo()
    return repo.create_task(task)

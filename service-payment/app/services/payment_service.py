import random
import time
from datetime import datetime
from typing import List

from app.models.payment import Payment, PaymentStatus, PaymentMethod
from app.repositories.payment_repo import PaymentRepo
from app.repositories.task_repo import TaskRepo


class PaymentService:
    repo: PaymentRepo

    def __init__(self):
        self.repo = PaymentRepo()

    def select_payment_method(self, task_id: int, assigned_user_id: int, payment_method: PaymentMethod) -> Payment:
        # Get task to get customer_id and amount
        task_repo = TaskRepo()
        task = task_repo.get_task_by_id(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        amount = task.price

        # Check balance of customer
        if not self.repo.deduct_balance(task.customer_id, amount):
            raise ValueError(f"Insufficient balance for customer {task.customer_id}")

        payment = Payment(
            customer_user_id=task.customer_id,
            assigned_user_id=assigned_user_id,
            task_id=task_id,
            amount=amount,
            payment_method=payment_method,
            status=PaymentStatus.PENDING,
            created_at=datetime.now().isoformat()
        )
        return self.repo.create_payment(payment)

    def process_payment(self, payment_id: int) -> Payment:
        payment = self.repo.get_payment(payment_id)
        if not payment:
            raise KeyError(f"Payment {payment_id} not found")

        if payment.status != PaymentStatus.PENDING:
            raise ValueError(f"Payment is already {payment.status}")

        self.repo.update_payment_status(payment_id, PaymentStatus.PROCESSING)
        payment.status = PaymentStatus.PROCESSING

        time.sleep(0.1)  # Имитация задержки

        is_successful = random.random() > 0.1
        if is_successful:
            transaction_id = f"TXN-{random.randint(100000, 999999)}"
            completed_at = datetime.now()
            self.repo.update_payment_status(payment_id, PaymentStatus.COMPLETED, transaction_id, completed_at)
            payment.status = PaymentStatus.COMPLETED
            payment.transaction_id = transaction_id
            payment.completed_at = completed_at.isoformat()

            # Перевод денег от заказчика к исполнителю
            task_repo = TaskRepo()
            success = task_repo.transfer_payment(payment.customer_user_id, payment.assigned_user_id, payment.amount)
            if success:
                # Удаляем задачу после успешной оплаты и перевода денег
                task_repo.delete_task(payment.task_id)

                print("Payment transfer completed, balances updated, task deleted")
            else:
                print("Payment transfer failed - insufficient funds")

        else:
            completed_at = datetime.now()
            self.repo.update_payment_status(payment_id, PaymentStatus.FAILED, completed_at=completed_at)
            payment.status = PaymentStatus.FAILED
            payment.completed_at = completed_at.isoformat()

        return payment

    def get_payment(self, payment_id: int) -> Payment:
        payment = self.repo.get_payment(payment_id)
        if not payment:
            raise KeyError(f"Payment {payment_id} not found")
        return payment

    def get_all_payments(self) -> List[Payment]:
        return self.repo.get_all_payments()

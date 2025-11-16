"""
Репозиторий для работы с платежами
"""
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.payment import Payment as DBPayment
from app.models.payment import Payment as ModelPayment, PaymentStatus, PaymentMethod
from datetime import datetime


class PaymentRepo:
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def get_all_payments(self) -> list[ModelPayment]:
        payments = []
        for p in self.db.query(DBPayment).all():
            payments.append(ModelPayment(
                id=p.id,
                customer_user_id=p.customer_user_id,
                assigned_user_id=p.assigned_user_id,
                task_id=p.task_id,
                amount=p.amount,
                payment_method=p.payment_method,
                status=p.status,
                created_at=p.created_at.isoformat() if p.created_at else None,
                completed_at=p.completed_at.isoformat() if p.completed_at else None,
                transaction_id=p.transaction_id
            ))
        return payments

    def get_payment(self, payment_id: int) -> ModelPayment | None:
        db_payment = self.db.query(DBPayment).filter(DBPayment.id == payment_id).first()
        if db_payment:
            return ModelPayment(
                id=db_payment.id,
                customer_user_id=db_payment.customer_user_id,
                assigned_user_id=db_payment.assigned_user_id,
                task_id=db_payment.task_id,
                amount=db_payment.amount,
                payment_method=db_payment.payment_method,
                status=db_payment.status,
                created_at=db_payment.created_at.isoformat() if db_payment.created_at else None,
                completed_at=db_payment.completed_at.isoformat() if db_payment.completed_at else None,
                transaction_id=db_payment.transaction_id
            )
        return None

    def create_payment(self, payment: ModelPayment) -> ModelPayment:
        if payment.id:
            existing = self.db.query(DBPayment).filter(DBPayment.id == payment.id).first()
            if existing:
                raise KeyError(f"Payment {payment.id} already exists")

        db_payment = DBPayment(
            customer_user_id=payment.customer_user_id,
            assigned_user_id=payment.assigned_user_id,
            task_id=payment.task_id,
            amount=payment.amount,
            payment_method=payment.payment_method,
            status=payment.status,
            created_at=datetime.fromisoformat(payment.created_at) if payment.created_at else datetime.utcnow()
        )
        self.db.add(db_payment)
        self.db.commit()
        self.db.refresh(db_payment)
        return ModelPayment(
            id=db_payment.id,
            customer_user_id=db_payment.customer_user_id,
            assigned_user_id=db_payment.assigned_user_id,
            task_id=db_payment.task_id,
            amount=db_payment.amount,
            payment_method=db_payment.payment_method,
            status=db_payment.status,
            created_at=db_payment.created_at.isoformat() if db_payment.created_at else None,
            completed_at=db_payment.completed_at.isoformat() if db_payment.completed_at else None,
            transaction_id=db_payment.transaction_id
        )

    def update_payment_status(self, payment_id: int, status: PaymentStatus, transaction_id: str = None, completed_at: datetime = None):
        db_payment = self.db.query(DBPayment).filter(DBPayment.id == payment_id).first()
        if db_payment:
            db_payment.status = status
            if transaction_id:
                db_payment.transaction_id = transaction_id
            if completed_at:
                db_payment.completed_at = completed_at
            self.db.commit()

    def check_balance(self, user_id: int) -> float:
        # Use task repo to get real balance
        from .task_repo import TaskRepo
        task_repo = TaskRepo()
        return task_repo.get_balance(user_id)

    def deduct_balance(self, user_id: int, amount: float) -> bool:
        # Check if balance >= amount (for validation before payment)
        current_balance = self.check_balance(user_id)
        return current_balance >= amount

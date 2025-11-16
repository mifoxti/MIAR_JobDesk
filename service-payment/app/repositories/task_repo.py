"""
Репозиторий для работы с задачами (для тестирования)
"""
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.task import Task as DBTask
from app.models.task import Task as ModelTask

# In-memory storage for user balances (since no dedicated user service)
user_balances = {
    1: 500.0,
    2: 200.0,
    3: 1000.0,
    4: 750.0,
    5: 300.0
}


class TaskRepo:
    db: Session

    def __init__(self):
        self.db = next(get_db())

    def get_all_tasks(self) -> list[ModelTask]:
        tasks = []
        for t in self.db.query(DBTask).all():
            tasks.append(ModelTask.from_orm(t))
        return tasks

    def get_task_by_id(self, task_id: int) -> ModelTask | None:
        db_task = self.db.query(DBTask).filter(DBTask.id == task_id).first()
        return ModelTask.from_orm(db_task) if db_task else None

    def create_task(self, task: ModelTask) -> ModelTask:
        db_task = DBTask(
            title=task.title,
            description=task.description,
            price=task.price,
            customer_id=task.customer_id
        )
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return ModelTask.from_orm(db_task)

    def get_balance(self, user_id: int) -> float:
        return user_balances.get(user_id, 0.0)

    def transfer_payment(self, from_user: int, to_user: int, amount: float) -> bool:
        from_balance = self.get_balance(from_user)
        if from_balance >= amount:
            # Выполняем реальный перевод
            user_balances[from_user] -= amount
            user_balances[to_user] += amount
            print(f"Transferred {amount} from user {from_user} to user {to_user}")
            print(f"New balances: User {from_user}: {user_balances[from_user]}, User {to_user}: {user_balances[to_user]}")
            return True
        return False

    def check_balance_for_transfer(self, user_id: int) -> float:
        return self.get_balance(user_id)

    def delete_task(self, task_id: int) -> bool:
        db_task = self.db.query(DBTask).filter(DBTask.id == task_id).first()
        if db_task:
            self.db.delete(db_task)
            self.db.commit()
            print(f"Task {task_id} deleted after successful payment")
            return True
        return False

    def update_balance(self, user_id: int, amount: float) -> bool:
        # Update balance by adding/subtracting amount
        user_balances[user_id] += amount
        print(f"Balance updated for user {user_id}: {user_balances[user_id]} (change: {amount})")
        return True

    def get_all_balances(self) -> dict:
        return user_balances.copy()

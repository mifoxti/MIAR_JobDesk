class Payment:
    def __init__(self, id: int, user_id: int, task_id: int, amount: float,
                 payment_method: str, status: str = 'pending',
                 created_at: str = None, completed_at: str = None,
                 transaction_id: str = None):
        self._id = id
        self._user_id = user_id
        self._task_id = task_id
        self._amount = amount
        self._payment_method = payment_method
        self._status = status
        self._created_at = created_at
        self._completed_at = completed_at
        self._transaction_id = transaction_id
        
        # Валидация статуса
        valid_statuses = ['pending', 'processing', 'completed', 'failed', 'cancelled']
        if self._status not in valid_statuses:
            raise ValueError(f"Status must be one of {valid_statuses}, got '{self._status}'")
        
        # Валидация способа оплаты
        valid_methods = ['card', 'bank_transfer', 'electronic_wallet', 'crypto']
        if self._payment_method not in valid_methods:
            raise ValueError(f"Payment method must be one of {valid_methods}, got '{self._payment_method}'")

    def to_dict(self):
        return {
            "id": self._id,
            "user_id": self._user_id,
            "task_id": self._task_id,
            "amount": self._amount,
            "payment_method": self._payment_method,
            "status": self._status,
            "created_at": self._created_at,
            "completed_at": self._completed_at,
            "transaction_id": self._transaction_id
        }



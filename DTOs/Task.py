class Task:
    def __init__(self, id: int, title: str, created_by_user_id: int,
                 description: str = None, accepted_by_user_id: int = None,
                 status: str = 'open', price: float = None, deadline: str = None,
                 created_at: str = None, updated_at: str = None):
        self._id = id
        self._title = title
        self._description = description
        self._created_by_user_id = created_by_user_id
        self._accepted_by_user_id = accepted_by_user_id
        self._status = status
        self._price = price
        self._deadline = deadline
        self._created_at = created_at
        self._updated_at = updated_at
        
        # Валидация статуса
        valid_statuses = ['open', 'in_progress', 'completed', 'cancelled']
        if self._status not in valid_statuses:
            raise ValueError(f"Status must be one of {valid_statuses}, got '{self._status}'")

    def to_dict(self):
        return {
            "id": self._id,
            "title": self._title,
            "description": self._description,
            "created_by_user_id": self._created_by_user_id,
            "accepted_by_user_id": self._accepted_by_user_id,
            "status": self._status,
            "price": self._price,
            "deadline": self._deadline,
            "created_at": self._created_at,
            "updated_at": self._updated_at
        }


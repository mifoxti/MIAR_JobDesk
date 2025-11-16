from pydantic import BaseModel, ConfigDict
from typing import Optional


class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    title: str
    description: str
    price: float
    customer_id: int  # Заказчик

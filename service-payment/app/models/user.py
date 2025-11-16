from pydantic import BaseModel, ConfigDict
from typing import Optional


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    first_name: str
    last_name: str
    balance: float

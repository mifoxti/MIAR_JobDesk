from pydantic import BaseModel, ConfigDict

class Notification(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    recipient_id: int
    message: str
    type: str  # например, 'new_message', 'new_response', 'response_rejected', 'response_accepted', 'task_completed', 'rating_changed'

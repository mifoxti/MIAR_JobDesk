class Notification:
    def __init__(self, recipient_id: int, message: str, type: str):
        self._recipient_id = recipient_id
        self._message = message
        self._type = type  # например, 'new_message', 'new_response', 'response_rejected', 'response_accepted', 'task_completed', 'rating_changed'

    @property
    def recipient_id(self):
        return self._recipient_id

    @property
    def message(self):
        return self._message

    @property
    def type(self):
        return self._type

    def to_dict(self):
        return {
            "recipient_id": self._recipient_id,
            "message": self._message,
            "type": self._type
        }

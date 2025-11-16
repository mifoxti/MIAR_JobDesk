from app.models.notification import Notification


class NotificationService:
    """
    Сервис для обработки уведомлений
    """

    def send_new_message_notification(self, recipient_id: int, sender_name: str) -> Notification:
        message = f"У вас новое сообщение от {sender_name}"
        return self._send_notification(recipient_id, message, "new_message")

    def send_new_response_notification(self, recipient_id: int, responder_name: str) -> Notification:
        message = f"У вас новый отклик от {responder_name}"
        return self._send_notification(recipient_id, message, "new_response")

    def send_response_rejected_notification(self, recipient_id: int) -> Notification:
        message = "Ваш отклик был отклонен"
        return self._send_notification(recipient_id, message, "response_rejected")

    def send_response_accepted_notification(self, recipient_id: int) -> Notification:
        message = "Ваш отклик был принят"
        return self._send_notification(recipient_id, message, "response_accepted")

    def send_task_completed_notification(self, recipient_id: int, task_title: str) -> Notification:
        message = f"Работа '{task_title}' выполнена"
        return self._send_notification(recipient_id, message, "task_completed")

    def send_rating_changed_notification(self, recipient_id: int, new_rating: float) -> Notification:
        message = f"Ваш рейтинг обновлен: {new_rating}"
        return self._send_notification(recipient_id, message, "rating_changed")

    def _send_notification(self, recipient_id: int, message: str, notification_type: str) -> Notification:
        notification = Notification(recipient_id=recipient_id, message=message, type=notification_type)
        # TODO: Интегрировать с email сервисом или RabbitMQ для публикации
        print(f"Sending notification: {notification}")
        return notification

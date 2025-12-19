import asyncio
from app.models.notification import Notification
from app.services.external_email_service import send_notification_email
from app.logging_config import get_logger

logger = get_logger(__name__)


class NotificationService:
    """
    Сервис для обработки уведомлений
    Интегрирован с внешним email сервисом с паттернами отказоустойчивости
    """

    async def send_new_message_notification(self, recipient_id: int, sender_name: str) -> Notification:
        message = f"У вас новое сообщение от {sender_name}"
        return await self._send_notification(recipient_id, message, "new_message")

    async def send_new_response_notification(self, recipient_id: int, responder_name: str) -> Notification:
        message = f"У вас новый отклик от {responder_name}"
        return await self._send_notification(recipient_id, message, "new_response")

    async def send_response_rejected_notification(self, recipient_id: int) -> Notification:
        message = "Ваш отклик был отклонен"
        return await self._send_notification(recipient_id, message, "response_rejected")

    async def send_response_accepted_notification(self, recipient_id: int) -> Notification:
        message = "Ваш отклик был принят"
        return await self._send_notification(recipient_id, message, "response_accepted")

    async def send_task_completed_notification(self, recipient_id: int, task_title: str) -> Notification:
        message = f"Работа '{task_title}' выполнена"
        return await self._send_notification(recipient_id, message, "task_completed")

    async def send_rating_changed_notification(self, recipient_id: int, new_rating: float) -> Notification:
        message = f"Ваш рейтинг обновлен: {new_rating}"
        return await self._send_notification(recipient_id, message, "rating_changed")

    async def _send_notification(self, recipient_id: int, message: str, notification_type: str) -> Notification:
        """
        Отправка уведомления через внешний email сервис
        Использует паттерны отказоустойчивости: Circuit Breaker, Retry, Timeout
        """
        notification = Notification(
            recipient_id=recipient_id,
            message=message,
            type=notification_type
        )

        logger.info(
            "preparing_notification",
            recipient_id=recipient_id,
            notification_type=notification_type
        )

        # Отправка через внешний email сервис с паттернами отказоустойчивости
        email_result = await send_notification_email(
            recipient=f"user_{recipient_id}@example.com",
            subject=f"Notification: {notification_type}",
            body=message,
            use_mock=True  # Используем mock для демонстрации
        )

        if email_result.get("success"):
            logger.info(
                "notification_sent_successfully",
                recipient_id=recipient_id,
                notification_type=notification_type,
                message_id=email_result.get("message_id")
            )
        else:
            logger.error(
                "notification_sending_failed",
                recipient_id=recipient_id,
                notification_type=notification_type,
                error=email_result.get("error")
            )

        return notification

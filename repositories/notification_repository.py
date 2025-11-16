"""
Репозиторий для работы с уведомлениями
"""
from DTOs.Notification import Notification
from repositories.user_repository import get_user_by_id


def send_notification(recipient_id: int, message: str, notification_type: str) -> Notification:
    """
    Отправить уведомление пользователю.
    Пока просто создает объект уведомления, но в будущем можно добавить отправку email/SMS.

    Args:
        recipient_id: ID получателя
        message: Текст уведомления
        notification_type: Тип уведомления ('new_message', 'new_response', 'response_rejected',
                            'response_accepted', 'task_completed', 'rating_changed')

    Returns:
        Объект Notification

    Raises:
        ValueError: Если пользователь не найден
    """
    user = get_user_by_id(recipient_id)
    if not user:
        raise ValueError(f"User with id {recipient_id} not found")

    notification = Notification(recipient_id, message, notification_type)
    # TODO: Интегрировать с email сервисом или другим способом доставки уведомлений

    print(f"Sending notification to user {recipient_id}: {message}")  # Заглушка
    return notification

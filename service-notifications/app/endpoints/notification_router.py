from fastapi import APIRouter, Depends

from app.services.notification_service import NotificationService
from app.models.notification import Notification

notification_router = APIRouter(prefix='/notifications', tags=['Notifications'])


@notification_router.post("/send-new-message", response_model=Notification, summary="Отправить уведомление о новом сообщении")
def send_new_message_notification(
    recipient_id: int,
    sender_name: str,
    service: NotificationService = Depends()
):
    """
    Отправляет уведомление пользователю о новом сообщении.

    - **recipient_id**: ID получателя уведомления
    - **sender_name**: Имя отправителя сообщения
    """
    return service.send_new_message_notification(recipient_id, sender_name)


@notification_router.post("/send-new-response", response_model=Notification, summary="Отправить уведомление о новом отклике")
def send_new_response_notification(
    recipient_id: int,
    responder_name: str,
    service: NotificationService = Depends()
):
    """
    Отправляет уведомление пользователю о новом отклике на задачу.

    - **recipient_id**: ID получателя уведомления
    - **responder_name**: Имя пользователя, приславшего отклик
    """
    return service.send_new_response_notification(recipient_id, responder_name)


@notification_router.post("/send-response-rejected", response_model=Notification, summary="Отправить уведомление об отклонении отклика")
def send_response_rejected_notification(
    recipient_id: int,
    service: NotificationService = Depends()
):
    """
    Отправляет уведомление пользователю об отклонении его отклика.

    - **recipient_id**: ID получателя уведомления
    """
    return service.send_response_rejected_notification(recipient_id)


@notification_router.post("/send-response-accepted", response_model=Notification, summary="Отправить уведомление о принятии отклика")
def send_response_accepted_notification(
    recipient_id: int,
    service: NotificationService = Depends()
):
    """
    Отправляет уведомление пользователю о принятии его отклика.

    - **recipient_id**: ID получателя уведомления
    """
    return service.send_response_accepted_notification(recipient_id)


@notification_router.post("/send-task-completed", response_model=Notification, summary="Отправить уведомление о выполнении задачи")
def send_task_completed_notification(
    recipient_id: int,
    task_title: str,
    service: NotificationService = Depends()
):
    """
    Отправляет уведомление пользователю о выполнении задачи.

    - **recipient_id**: ID получателя уведомления
    - **task_title**: Название выполненной задачи
    """
    return service.send_task_completed_notification(recipient_id, task_title)


@notification_router.post("/send-rating-changed", response_model=Notification, summary="Отправить уведомление об изменении рейтинга")
def send_rating_changed_notification(
    recipient_id: int,
    new_rating: float,
    service: NotificationService = Depends()
):
    """
    Отправляет уведомление пользователю об изменении его рейтинга.

    - **recipient_id**: ID получателя уведомления
    - **new_rating**: Новый рейтинг пользователя (число с плавающей точкой)
    """
    return service.send_rating_changed_notification(recipient_id, new_rating)

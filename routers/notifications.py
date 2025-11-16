"""
Роутеры для работы с уведомлениями
"""
from fastapi import APIRouter, HTTPException
from repositories.notification_repository import send_notification
from repositories.user_repository import update_user_rating
from typing import Dict

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("/send-new-message", response_model=Dict)
def send_new_message_notification(recipient_id: int, sender_name: str):
    """
    Отправить уведомление о новом сообщении

    Args:
        recipient_id: ID получателя
        sender_name: Имя отправителя

    Returns:
        Словарь с деталями уведомления
    """
    try:
        message = f"У вас новое сообщение от {sender_name}"
        notification = send_notification(recipient_id, message, "new_message")
        return notification.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending notification: {str(e)}")


@router.post("/send-new-response", response_model=Dict)
def send_new_response_notification(recipient_id: int, responder_name: str):
    """
    Отправить уведомление о новом отклике

    Args:
        recipient_id: ID получателя
        responder_name: Имя откликнувшегося

    Returns:
        Словарь с деталями уведомления
    """
    try:
        message = f"У вас новый отклик от {responder_name}"
        notification = send_notification(recipient_id, message, "new_response")
        return notification.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending notification: {str(e)}")


@router.post("/send-response-rejected", response_model=Dict)
def send_response_rejected_notification(recipient_id: int):
    """
    Отправить уведомление об отклоеннии отклика

    Args:
        recipient_id: ID получателя

    Returns:
        Словарь с деталями уведомления
    """
    try:
        message = "Ваш отклик был отклонен"
        notification = send_notification(recipient_id, message, "response_rejected")
        return notification.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending notification: {str(e)}")


@router.post("/send-response-accepted", response_model=Dict)
def send_response_accepted_notification(recipient_id: int):
    """
    Отправить уведомление о принятии отклика

    Args:
        recipient_id: ID получателя

    Returns:
        Словарь с деталями уведомления
    """
    try:
        message = "Ваш отклик был принят"
        notification = send_notification(recipient_id, message, "response_accepted")
        return notification.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending notification: {str(e)}")


@router.post("/send-task-completed", response_model=Dict)
def send_task_completed_notification(recipient_id: int, task_title: str):
    """
    Отправить уведомление о выполнении работы

    Args:
        recipient_id: ID получателя
        task_title: Название задачи

    Returns:
        Словарь с деталями уведомления
    """
    try:
        message = f"Работа '{task_title}' выполнена"
        notification = send_notification(recipient_id, message, "task_completed")
        return notification.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending notification: {str(e)}")


@router.post("/send-rating-changed", response_model=Dict)
def send_rating_changed_notification(recipient_id: int, new_rating: float):
    """
    Отправить уведомление об изменении репутации и обновить рейтинг

    Args:
        recipient_id: ID получателя
        new_rating: Новый рейтинг

    Returns:
        Словарь с деталями уведомления
    """
    try:
        # Обновить рейтинг в БД
        success = update_user_rating(recipient_id, new_rating)
        if not success:
            raise ValueError(f"Failed to update rating for user {recipient_id}")

        message = f"Ваш рейтинг обновлен: {new_rating}"
        notification = send_notification(recipient_id, message, "rating_changed")
        return notification.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending notification: {str(e)}")

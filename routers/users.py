"""
Роутеры для работы с пользователями
"""
from fastapi import APIRouter, HTTPException
from typing import List
from repositories.user_repository import get_all_users, get_user_by_id

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[dict])
def get_all_users_endpoint():
    """
    Получить список всех пользователей
    
    Returns:
        Список всех пользователей
    """
    try:
        users = get_all_users()
        return [user.to_dict() for user in users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")


@router.get("/{user_id}", response_model=dict)
def get_user_by_id_endpoint(user_id: int):
    """
    Получить пользователя по ID
    
    Args:
        user_id: ID пользователя
        
    Returns:
        Информация о пользователе
        
    Raises:
        HTTPException: Если пользователь не найден
    """
    try:
        user = get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
        return user.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")


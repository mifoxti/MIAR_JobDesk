"""
Роутеры для работы с задачами
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from repositories.task_repository import (
    get_all_tasks,
    get_task_by_id,
    get_tasks_by_user_id,
    get_tasks_by_status,
    get_tasks_by_accepted_user_id
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[dict])
def get_tasks_endpoint(status: Optional[str] = None, user_id: Optional[int] = None, accepted_by: Optional[int] = None):
    """
    Получить список всех задач
    
    Query параметры:
        status: Фильтр по статусу (open, in_progress, completed, cancelled)
        user_id: Фильтр по ID создателя задачи
        accepted_by: Фильтр по ID пользователя, принявшего задачу
    
    Returns:
        Список задач
    """
    try:
        if status:
            tasks = get_tasks_by_status(status)
        elif user_id:
            tasks = get_tasks_by_user_id(user_id)
        elif accepted_by:
            tasks = get_tasks_by_accepted_user_id(accepted_by)
        else:
            tasks = get_all_tasks()
        
        return [task.to_dict() for task in tasks]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tasks: {str(e)}")


@router.get("/{task_id}", response_model=dict)
def get_task_by_id_endpoint(task_id: int):
    """
    Получить задачу по ID
    
    Args:
        task_id: ID задачи
        
    Returns:
        Информация о задаче
        
    Raises:
        HTTPException: Если задача не найдена
    """
    try:
        task = get_task_by_id(task_id)
        if task is None:
            raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
        return task.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching task: {str(e)}")


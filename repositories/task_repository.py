"""
Репозиторий для работы с задачами в базе данных
"""
from typing import List, Optional
from database.connection import get_db_cursor
from DTOs.Task import Task


def _decode_string(value):
    """
    Декодирует строковое значение из БД в UTF-8
    После пересоздания БД с правильной кодировкой и регистрации UNICODE типов
    данные должны приходить уже в правильной кодировке
    
    Args:
        value: Значение из БД (может быть str, bytes или None)
        
    Returns:
        Строка в UTF-8 или исходное значение
    """
    if value is None:
        return None
    
    # Если это bytes, декодируем через UTF-8
    if isinstance(value, bytes):
        try:
            return value.decode('utf-8')
        except UnicodeDecodeError:
            return value.decode('utf-8', errors='replace')
    
    # Если это уже строка, возвращаем как есть
    # После регистрации UNICODE типов и правильной настройки БД
    # данные должны приходить уже в правильной кодировке
    return value


def get_all_tasks() -> List[Task]:
    """
    Получить все задачи из базы данных
    
    Returns:
        Список объектов Task
    """
    with get_db_cursor(dict_cursor=True) as cursor:
        cursor.execute('SELECT * FROM Task ORDER BY id')
        tasks_data = cursor.fetchall()
        
        tasks = []
        for task_data in tasks_data:
            task = Task(
                id=task_data['id'],
                title=_decode_string(task_data['title']),
                created_by_user_id=task_data['created_by_user_id'],
                description=_decode_string(task_data['description']) if task_data['description'] else None,
                accepted_by_user_id=task_data['accepted_by_user_id'] if task_data['accepted_by_user_id'] else None,
                status=_decode_string(task_data['status']),
                price=float(task_data['price']) if task_data['price'] else None,
                deadline=str(task_data['deadline']) if task_data['deadline'] else None,
                created_at=str(task_data['created_at']) if task_data['created_at'] else None,
                updated_at=str(task_data['updated_at']) if task_data['updated_at'] else None
            )
            tasks.append(task)
        
        return tasks


def get_task_by_id(task_id: int) -> Optional[Task]:
    """
    Получить задачу по ID
    
    Args:
        task_id: ID задачи
        
    Returns:
        Объект Task или None, если задача не найдена
    """
    with get_db_cursor(dict_cursor=True) as cursor:
        cursor.execute('SELECT * FROM Task WHERE id = %s', (task_id,))
        task_data = cursor.fetchone()
        
        if task_data is None:
            return None
        
        task = Task(
            id=task_data['id'],
            title=_decode_string(task_data['title']),
            created_by_user_id=task_data['created_by_user_id'],
            description=_decode_string(task_data['description']) if task_data['description'] else None,
            accepted_by_user_id=task_data['accepted_by_user_id'] if task_data['accepted_by_user_id'] else None,
            status=_decode_string(task_data['status']),
            price=float(task_data['price']) if task_data['price'] else None,
            deadline=str(task_data['deadline']) if task_data['deadline'] else None,
            created_at=str(task_data['created_at']) if task_data['created_at'] else None,
            updated_at=str(task_data['updated_at']) if task_data['updated_at'] else None
        )
        
        return task


def get_tasks_by_user_id(user_id: int) -> List[Task]:
    """
    Получить все задачи, созданные пользователем
    
    Args:
        user_id: ID пользователя
        
    Returns:
        Список объектов Task
    """
    with get_db_cursor(dict_cursor=True) as cursor:
        cursor.execute('SELECT * FROM Task WHERE created_by_user_id = %s ORDER BY id', (user_id,))
        tasks_data = cursor.fetchall()
        
        tasks = []
        for task_data in tasks_data:
            task = Task(
                id=task_data['id'],
                title=_decode_string(task_data['title']),
                created_by_user_id=task_data['created_by_user_id'],
                description=_decode_string(task_data['description']) if task_data['description'] else None,
                accepted_by_user_id=task_data['accepted_by_user_id'] if task_data['accepted_by_user_id'] else None,
                status=_decode_string(task_data['status']),
                price=float(task_data['price']) if task_data['price'] else None,
                deadline=str(task_data['deadline']) if task_data['deadline'] else None,
                created_at=str(task_data['created_at']) if task_data['created_at'] else None,
                updated_at=str(task_data['updated_at']) if task_data['updated_at'] else None
            )
            tasks.append(task)
        
        return tasks


def get_tasks_by_status(status: str) -> List[Task]:
    """
    Получить все задачи по статусу
    
    Args:
        status: Статус задачи (open, in_progress, completed, cancelled)
        
    Returns:
        Список объектов Task
    """
    with get_db_cursor(dict_cursor=True) as cursor:
        cursor.execute('SELECT * FROM Task WHERE status = %s ORDER BY id', (status,))
        tasks_data = cursor.fetchall()
        
        tasks = []
        for task_data in tasks_data:
            task = Task(
                id=task_data['id'],
                title=_decode_string(task_data['title']),
                created_by_user_id=task_data['created_by_user_id'],
                description=_decode_string(task_data['description']) if task_data['description'] else None,
                accepted_by_user_id=task_data['accepted_by_user_id'] if task_data['accepted_by_user_id'] else None,
                status=_decode_string(task_data['status']),
                price=float(task_data['price']) if task_data['price'] else None,
                deadline=str(task_data['deadline']) if task_data['deadline'] else None,
                created_at=str(task_data['created_at']) if task_data['created_at'] else None,
                updated_at=str(task_data['updated_at']) if task_data['updated_at'] else None
            )
            tasks.append(task)
        
        return tasks


def get_tasks_by_accepted_user_id(user_id: int) -> List[Task]:
    """
    Получить все задачи, принятые пользователем
    
    Args:
        user_id: ID пользователя
        
    Returns:
        Список объектов Task
    """
    with get_db_cursor(dict_cursor=True) as cursor:
        cursor.execute('SELECT * FROM Task WHERE accepted_by_user_id = %s ORDER BY id', (user_id,))
        tasks_data = cursor.fetchall()
        
        tasks = []
        for task_data in tasks_data:
            task = Task(
                id=task_data['id'],
                title=_decode_string(task_data['title']),
                created_by_user_id=task_data['created_by_user_id'],
                description=_decode_string(task_data['description']) if task_data['description'] else None,
                accepted_by_user_id=task_data['accepted_by_user_id'] if task_data['accepted_by_user_id'] else None,
                status=_decode_string(task_data['status']),
                price=float(task_data['price']) if task_data['price'] else None,
                deadline=str(task_data['deadline']) if task_data['deadline'] else None,
                created_at=str(task_data['created_at']) if task_data['created_at'] else None,
                updated_at=str(task_data['updated_at']) if task_data['updated_at'] else None
            )
            tasks.append(task)
        
        return tasks



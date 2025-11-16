"""
Репозиторий для работы с пользователями в базе данных
"""
from typing import List, Optional
from database.connection import get_db_cursor
from DTOs.User import User


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


def get_all_users() -> List[User]:
    """
    Получить всех пользователей из базы данных
    
    Returns:
        Список объектов User
    """
    with get_db_cursor(dict_cursor=True) as cursor:
        cursor.execute('SELECT * FROM "User" ORDER BY id')
        users_data = cursor.fetchall()
        
        users = []
        for user_data in users_data:
            user = User(
                id=user_data['id'],
                first_name=_decode_string(user_data['first_name']),
                last_name=_decode_string(user_data['last_name']),
                middle_name=_decode_string(user_data['middle_name']) if user_data['middle_name'] else None,
                email=_decode_string(user_data['email']),
                phone=_decode_string(user_data['phone']) if user_data['phone'] else None,
                order_count=user_data['order_count'],
                balance=float(user_data['balance']),
                registration_date=str(user_data['registration_date']),
                last_login=str(user_data['last_login']) if user_data['last_login'] else None,
                is_active=user_data['is_active'],
                password=_decode_string(user_data.get('password', '')),
                rating=float(user_data.get('rating', 0.0))
            )
            users.append(user)
        
        return users


def get_user_by_id(user_id: int) -> Optional[User]:
    """
    Получить пользователя по ID
    
    Args:
        user_id: ID пользователя
        
    Returns:
        Объект User или None, если пользователь не найден
    """
    with get_db_cursor(dict_cursor=True) as cursor:
        cursor.execute('SELECT * FROM "User" WHERE id = %s', (user_id,))
        user_data = cursor.fetchone()
        
        if user_data is None:
            return None
        
        user = User(
            id=user_data['id'],
            first_name=_decode_string(user_data['first_name']),
            last_name=_decode_string(user_data['last_name']),
            middle_name=_decode_string(user_data['middle_name']) if user_data['middle_name'] else None,
            email=_decode_string(user_data['email']),
            phone=_decode_string(user_data['phone']) if user_data['phone'] else None,
            order_count=user_data['order_count'],
            balance=float(user_data['balance']),
            registration_date=str(user_data['registration_date']),
            last_login=str(user_data['last_login']) if user_data['last_login'] else None,
            is_active=user_data['is_active'],
            password=_decode_string(user_data.get('password', '')),
            rating=float(user_data.get('rating', 0.0))
        )

        return user


def update_user_rating(user_id: int, new_rating: float) -> bool:
    """
    Обновить рейтинг пользователя

    Args:
        user_id: ID пользователя
        new_rating: Новый рейтинг

    Returns:
        True если обновление успешно, False если пользователь не найден
    """
    with get_db_cursor() as cursor:
        cursor.execute('UPDATE "User" SET rating = %s WHERE id = %s', (new_rating, user_id))
        return cursor.rowcount > 0


def get_user_by_email(email: str) -> Optional[User]:
    """
    Получить пользователя по email
    
    Args:
        email: Email пользователя
        
    Returns:
        Объект User или None, если пользователь не найден
    """
    with get_db_cursor(dict_cursor=True) as cursor:
        cursor.execute('SELECT * FROM "User" WHERE email = %s', (email,))
        user_data = cursor.fetchone()
        
        if user_data is None:
            return None
        
        user = User(
            id=user_data['id'],
            first_name=_decode_string(user_data['first_name']),
            last_name=_decode_string(user_data['last_name']),
            middle_name=_decode_string(user_data['middle_name']) if user_data['middle_name'] else None,
            email=_decode_string(user_data['email']),
            phone=_decode_string(user_data['phone']) if user_data['phone'] else None,
            order_count=user_data['order_count'],
            balance=float(user_data['balance']),
            registration_date=str(user_data['registration_date']),
            last_login=str(user_data['last_login']) if user_data['last_login'] else None,
            is_active=user_data['is_active'],
            password=_decode_string(user_data.get('password', '')),
            rating=float(user_data.get('rating', 0.0))
        )

        return user

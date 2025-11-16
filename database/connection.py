"""
Модуль для работы с подключением к базе данных PostgreSQL
"""
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import register_type, UNICODE
from psycopg2.extensions import register_adapter, AsIs
from contextlib import contextmanager
from typing import Optional
from database.config import DATABASE_URL, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

# Регистрируем типы для правильной работы с Unicode
# Это гарантирует, что все текстовые данные будут правильно декодироваться
try:
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
except:
    pass


class DatabaseConnection:
    """Класс для управления подключением к базе данных"""
    
    _connection_pool: Optional[pool.ThreadedConnectionPool] = None
    
    @classmethod
    def initialize_pool(cls, min_conn: int = 1, max_conn: int = 10):
        """Инициализация пула соединений"""
        try:
            cls._connection_pool = pool.ThreadedConnectionPool(
                min_conn,
                max_conn,
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                client_encoding='UTF8'  # Устанавливаем кодировку UTF-8
            )
            print("Database connection pool created successfully")
        except Exception as e:
            print(f"Error creating connection pool: {e}")
            raise
    
    @classmethod
    def get_connection(cls):
        """Получить соединение из пула"""
        if cls._connection_pool is None:
            cls.initialize_pool()
        return cls._connection_pool.getconn()
    
    @classmethod
    def return_connection(cls, conn):
        """Вернуть соединение в пул"""
        if cls._connection_pool:
            cls._connection_pool.putconn(conn)
    
    @classmethod
    def close_all_connections(cls):
        """Закрыть все соединения в пуле"""
        if cls._connection_pool:
            cls._connection_pool.closeall()
            cls._connection_pool = None
            print("All database connections closed")


@contextmanager
def get_db_connection():
    """
    Контекстный менеджер для работы с базой данных.
    Автоматически закрывает соединение после использования.
    
    Пример использования:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            result = cursor.fetchall()
    """
    conn = None
    try:
        conn = DatabaseConnection.get_connection()
        # Устанавливаем кодировку UTF-8 для соединения
        conn.set_client_encoding('UTF8')
        yield conn
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Database error: {e}")
        raise
    finally:
        if conn:
            DatabaseConnection.return_connection(conn)


@contextmanager
def get_db_cursor(dict_cursor: bool = False):
    """
    Контекстный менеджер для работы с курсором базы данных.
    Автоматически закрывает курсор и соединение.
    
    Args:
        dict_cursor: Если True, возвращает RealDictCursor (результаты как словари)
    
    Пример использования:
        with get_db_cursor(dict_cursor=True) as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            result = cursor.fetchone()
    """
    conn = None
    cursor = None
    try:
        conn = DatabaseConnection.get_connection()
        # Устанавливаем кодировку UTF-8 для соединения
        conn.set_client_encoding('UTF8')
        # Включаем автоматическое декодирование Unicode
        register_type(UNICODE, conn)
        if dict_cursor:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
        else:
            cursor = conn.cursor()
        # Дополнительно устанавливаем кодировку через SQL
        cursor.execute("SET client_encoding = 'UTF8'")
        yield cursor
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Database error: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            DatabaseConnection.return_connection(conn)


def test_connection():
    """Тестовая функция для проверки подключения к БД"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"PostgreSQL version: {version[0]}")
            print("Database connection successful!")
            return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False


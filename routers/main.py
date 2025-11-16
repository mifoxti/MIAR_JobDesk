"""
Основные роутеры приложения
"""
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["main"])


@router.get("/")
def root():
    """
    Корневой эндпоинт приложения
    
    Returns:
        HTML страница с приветствием
    """
    html_content = "<h2>Hello METANIT.COM!</h2>"
    return HTMLResponse(content=html_content)


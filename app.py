from fastapi import FastAPI
from routers import main, users, tasks

# Создание экземпляра приложения FastAPI
app = FastAPI(
    title="JobDesk API",
    description="API for the JobDesk project",
    version="1.0.0"
)

# Устанавливаем кодировку UTF-8 для всех ответов
@app.middleware("http")
async def add_charset_header(request, call_next):
    response = await call_next(request)
    if response.headers.get("content-type", "").startswith("application/json"):
        response.headers["content-type"] = "application/json; charset=utf-8"
    return response

# Подключение роутеров
app.include_router(main.router)
app.include_router(users.router)
app.include_router(tasks.router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

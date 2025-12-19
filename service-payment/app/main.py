import asyncio
import time
from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, Histogram, Gauge, CONTENT_TYPE_LATEST, generate_latest

from app import rabbitmq
from app.database import create_tables
from app.endpoints.payment_router import payment_router
from app.logging_config import configure_logging, get_logger

# Инициализация логирования
logger = configure_logging()

app = FastAPI(title='Payment Service')

# Создаем Prometheus метрики вручную
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

http_requests_inprogress = Gauge(
    'http_requests_inprogress',
    'HTTP requests in progress',
    ['method', 'endpoint']
)


@app.middleware("http")
async def logging_and_metrics_middleware(request: Request, call_next):
    """Middleware для логирования и сбора метрик HTTP запросов"""
    request_id = request.headers.get("X-Request-ID", str(time.time()))
    endpoint = request.url.path
    method = request.method

    log = get_logger().bind(
        request_id=request_id,
        method=method,
        path=endpoint,
        service="payment-service"
    )

    # Увеличиваем счетчик запросов в процессе
    http_requests_inprogress.labels(method=method, endpoint=endpoint).inc()

    start_time = time.time()
    log.info("request_started")

    try:
        response = await call_next(request)
        process_time = time.time() - start_time

        # Записываем метрики
        http_requests_total.labels(
            method=method,
            endpoint=endpoint,
            status_code=response.status_code
        ).inc()

        http_request_duration_seconds.labels(
            method=method,
            endpoint=endpoint
        ).observe(process_time)

        log.info(
            "request_completed",
            status_code=response.status_code,
            process_time=f"{process_time:.3f}s"
        )
        return response
    except Exception as e:
        process_time = time.time() - start_time

        # Записываем метрики ошибки
        http_requests_total.labels(
            method=method,
            endpoint=endpoint,
            status_code=500
        ).inc()

        log.error(
            "request_failed",
            error=str(e),
            process_time=f"{process_time:.3f}s"
        )
        raise
    finally:
        # Уменьшаем счетчик запросов в процессе
        http_requests_inprogress.labels(method=method, endpoint=endpoint).dec()


@app.on_event('startup')
def startup():
    log = get_logger().bind(service="payment-service")
    log.info("service_starting")
    log.info("prometheus_metrics_enabled", endpoint="/metrics")

    # Создать таблицы в БД перед запуском
    create_tables()
    log.info("database_tables_created")

    loop = asyncio.get_event_loop()
    asyncio.ensure_future(rabbitmq.consume(loop))
    log.info("rabbitmq_consumer_started")

    log.info("service_started")


@app.on_event('shutdown')
def shutdown():
    log = get_logger().bind(service="payment-service")
    log.info("service_shutdown")


@app.get("/health")
async def health_check():
    """Эндпоинт для проверки здоровья сервиса"""
    return {"status": "healthy", "service": "payment-service"}


app.include_router(payment_router, prefix='/api')

# Эндпоинт для экспорта метрик
@app.get("/metrics", include_in_schema=False)
async def metrics():
    """Эндпоинт для Prometheus метрик"""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

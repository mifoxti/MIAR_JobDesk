# MIAR Job Desk - Payment & Notification Microservices

Микросервисы для платформы MIAR Job Desk, предоставляющие функционал оплаты и уведомлений.

## Архитектура

- **service-payment**: Микросервис оплаты (FastAPI, PostgreSQL)
- **service-notifications**: Микросервис уведомлений (FastAPI, RabbitMQ)

## Установка и запуск

### Предварительные требования
- Docker и Docker Compose
- Python 3.10+

### Запуск сервисов
```bash
docker compose up --build
```

Сервисы будут доступны на:
- Payment API: http://localhost:8002/api/payment/
- Notifications API: http://localhost:8001/api/notifications/
- Swagger UI: http://localhost:8002/docs

## API Endpoints

### Payment Service

#### Основные эндпоинты
- `POST /api/payment/select-method` - Выбор способа оплаты
- `POST /api/payment/process` - Обработка платежа
- `GET /api/payment/{payment_id}` - Получение информации о платеже
- `GET /api/payment/` - Список всех платежей

#### Тестовые эндпоинты
- `GET /api/payment/test/users` - Получить тестовых пользователей с балансами
- `GET /api/payment/test/tasks` - Получить все тестовые задачи
- `POST /api/payment/test/create-task` - Создать тестовую задачу
- `GET /api/payment/users/{user_id}/balance` - Баланс конкретного пользователя
- `GET /api/payment/users/balances` - Балансы всех пользователей

### Notification Service

- `POST /api/notifications/payment-success` - Уведомление об успешной оплате
- `POST /api/notifications/payment-failed` - Уведомление о неудачной оплате
- `POST /api/notifications/task-completed` - Уведомление о выполнении задачи
- `POST /api/notifications/new-message` - Уведомление о новом сообщении

## Тестирование

### Unit Tests (Модульные тесты)

Запуск unit тестов для payment сервиса:
```bash
cd service-payment
pip install -r ../requirements.txt
pytest tests/ -v -m "not integration"
```

Запуск unit тестов для notification сервиса:
```bash
cd service-notifications
pytest tests/ -v
```

### Integration Tests (Интеграционные тесты)

```bash
cd service-payment
pytest tests/test_integrations.py -v
```

### Типы тестов

1. **Unit Tests**: Тестируют отдельные компоненты без внешних зависимостей
2. **Integration Tests**: Тестируют взаимодействие компонентов между собой
3. **Manual Tests**: Ручное тестирование через API/Swagger

### CI/CD

Тесты запускаются автоматически в GitHub Actions при push и PR.

```bash
.github/workflows/test.yml
```

## Бизнес-логика

### Процесс оплаты
1. **Создание задачи** заказчиком с указанием `customer_id`
2. **Выбор способа оплаты** с указанием `assigned_user_id` (исполнителя)
3. **Проверка баланса** заказчика перед созданием платежа
4. **Обработка платежа** (успех → перевод денег + удаление задачи)

### Балансы пользователей
- Реальные изменения происходят только при успешной оплате
- Баланс заказчика уменьшается на сумму платежа
- Баланс исполнителя увеличивается на сумму платежа

### Уведомления
- Автоматически отправляются при различных событиях
- Используют RabbitMQ для асинхронной доставки
- Поддерживают разные типы: оплата, задачи, сообщения

## Структура проекта

```
.
├── service-payment/
│   ├── app/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── services/
│   │   ├── endpoints/
│   │   └── database.py
│   └── tests/
├── service-notifications/
│   ├── app/
│   └── tests/
├── requirements.txt
├── pytest.ini
└── docker-compose.yml
```

## Запуск тестов в Docker

```bash
# Запустить все тесты в контейнерах
docker compose -f docker-compose.test.yml up --build

# Или запустить тесты отдельно после запуска сервисов
docker exec miar_jobdesk-service-payment pytest tests/ -v
```

## Метрики качества

- Code Coverage: минимум 80%
- Все тесты должны проходить в CI
- Линтинг кода согласно PEP 8
- Документированные API эндпоинты

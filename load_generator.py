"""
Скрипт для генерации нагрузки на микросервисы Payment и Notification
Используется для тестирования системы наблюдаемости (Prometheus + Grafana + Loki)
"""
import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor
import json

# URLs сервисов
PAYMENT_SERVICE = "http://localhost:8002"
NOTIFICATION_SERVICE = "http://localhost:8001"

def create_payment():
    """Создание платежа"""
    payload = {
        "amount": round(random.uniform(10.0, 1000.0), 2),
        "currency": random.choice(["USD", "EUR", "RUB"]),
        "user_id": random.randint(1, 100)
    }
    try:
        response = requests.post(
            f"{PAYMENT_SERVICE}/api/payments",
            json=payload,
            timeout=5
        )
        return f"✓ Payment created: {response.status_code}"
    except Exception as e:
        return f"✗ Payment failed: {e}"

def get_payments():
    """Получение списка платежей"""
    try:
        response = requests.get(f"{PAYMENT_SERVICE}/api/payments", timeout=5)
        return f"✓ Payments list: {response.status_code}"
    except Exception as e:
        return f"✗ Payments list failed: {e}"

def get_payment_by_id():
    """Получение платежа по ID"""
    payment_id = random.randint(1, 50)
    try:
        response = requests.get(f"{PAYMENT_SERVICE}/api/payments/{payment_id}", timeout=5)
        return f"✓ Payment {payment_id}: {response.status_code}"
    except Exception as e:
        return f"✗ Payment {payment_id} failed: {e}"

def send_notification():
    """Отправка уведомления"""
    payload = {
        "user_id": random.randint(1, 100),
        "message": f"Test notification {random.randint(1000, 9999)}",
        "channel": random.choice(["email", "sms", "push"])
    }
    try:
        response = requests.post(
            f"{NOTIFICATION_SERVICE}/api/notifications",
            json=payload,
            timeout=5
        )
        return f"✓ Notification sent: {response.status_code}"
    except Exception as e:
        return f"✗ Notification failed: {e}"

def get_notifications():
    """Получение списка уведомлений"""
    try:
        response = requests.get(f"{NOTIFICATION_SERVICE}/api/notifications", timeout=5)
        return f"✓ Notifications list: {response.status_code}"
    except Exception as e:
        return f"✗ Notifications list failed: {e}"

def health_check_payment():
    """Проверка здоровья Payment Service"""
    try:
        response = requests.get(f"{PAYMENT_SERVICE}/health", timeout=5)
        return f"✓ Payment health: {response.status_code}"
    except Exception as e:
        return f"✗ Payment health failed: {e}"

def health_check_notification():
    """Проверка здоровья Notification Service"""
    try:
        response = requests.get(f"{NOTIFICATION_SERVICE}/health", timeout=5)
        return f"✓ Notification health: {response.status_code}"
    except Exception as e:
        return f"✗ Notification health failed: {e}"

def run_load_test(duration_seconds=60, requests_per_second=5):
    """
    Запуск нагрузочного тестирования

    Args:
        duration_seconds: Длительность теста в секундах
        requests_per_second: Количество запросов в секунду
    """
    print(f"🚀 Запуск нагрузочного тестирования")
    print(f"⏱  Длительность: {duration_seconds} секунд")
    print(f"📊 Интенсивность: {requests_per_second} запросов/сек")
    print(f"📈 Всего запросов: ~{duration_seconds * requests_per_second}")
    print("-" * 60)

    # Список всех функций для запросов
    request_functions = [
        create_payment,
        get_payments,
        get_payment_by_id,
        send_notification,
        get_notifications,
        health_check_payment,
        health_check_notification,
    ]

    start_time = time.time()
    request_count = 0

    with ThreadPoolExecutor(max_workers=10) as executor:
        while time.time() - start_time < duration_seconds:
            # Выбираем случайные функции для выполнения
            functions_to_run = random.choices(
                request_functions,
                k=requests_per_second
            )

            # Запускаем запросы параллельно
            futures = [executor.submit(func) for func in functions_to_run]

            # Ждем результаты и выводим их
            for future in futures:
                result = future.result()
                request_count += 1
                if request_count % 10 == 0:
                    elapsed = time.time() - start_time
                    print(f"[{elapsed:.1f}s] {result} (всего: {request_count})")

            # Пауза для контроля интенсивности
            time.sleep(1)

    total_time = time.time() - start_time
    print("-" * 60)
    print(f"✅ Тест завершен!")
    print(f"📊 Статистика:")
    print(f"   - Общее время: {total_time:.2f} секунд")
    print(f"   - Всего запросов: {request_count}")
    print(f"   - Средняя скорость: {request_count/total_time:.2f} запросов/сек")

if __name__ == "__main__":
    # Проверка доступности сервисов
    print("🔍 Проверка доступности сервисов...")
    try:
        requests.get(f"{PAYMENT_SERVICE}/health", timeout=2)
        print("✓ Payment Service доступен")
    except:
        print("✗ Payment Service недоступен!")
        exit(1)

    try:
        requests.get(f"{NOTIFICATION_SERVICE}/health", timeout=2)
        print("✓ Notification Service доступен")
    except:
        print("✗ Notification Service недоступен!")
        exit(1)

    print()

    # Запуск нагрузочного теста
    # Можно изменить параметры: duration_seconds и requests_per_second
    run_load_test(duration_seconds=120, requests_per_second=8)

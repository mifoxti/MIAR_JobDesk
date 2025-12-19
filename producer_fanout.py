import pika
import sys

# Подключение
credentials = pika.PlainCredentials('guest', 'guest123')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='51.250.26.59',
        port=5672,
        credentials=credentials
    )
)
channel = connection.channel()

# Создаем обменник типа fanout
exchange_name = 'ikbo-06-22_lyakhov_fanout'
channel.exchange_declare(
    exchange=exchange_name,
    exchange_type='fanout',
    durable=True  # Сохраняемый обменник
)

# Текст сообщения из аргументов или по умолчанию
message_text = ' '.join(sys.argv[1:]) or 'Hello.#.World.#.#'

# Отправляем сообщение
channel.basic_publish(
    exchange=exchange_name,
    routing_key='',
    body=message_text,
    properties=pika.BasicProperties(
        delivery_mode=2  # Сохраняемое сообщение
    )
)

print(f"Sent: {message_text}")
connection.close()
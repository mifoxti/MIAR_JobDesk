import pika
import time

credentials = pika.PlainCredentials('guest', 'guest123')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='51.250.26.59',
        port=5672,
        credentials=credentials
    )
)
channel = connection.channel()

exchange_name = 'ikbo-06-22_lyakhov_fanout'
channel.exchange_declare(
    exchange=exchange_name,
    exchange_type='fanout',
    durable=True
)

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange=exchange_name, queue=queue_name)


def callback(ch, method, properties, body):
    message = body.decode()
    print(f"Received: {message}")

    sleep_time = message.count('#')
    print(f"Sleeping for {sleep_time} seconds...")
    time.sleep(sleep_time)

    print("Done processing")


channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True
)

print("Waiting for messages...")
channel.start_consuming()
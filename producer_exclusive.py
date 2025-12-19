import pika

credentials = pika.PlainCredentials('guest', 'guest123')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='51.250.26.59',
        port=5672,
        credentials=credentials
    )
)

channel = connection.channel()

channel.queue_declare(queue='ikbo-06-22_lyakhov', exclusive=True)

channel.basic_publish(
    exchange='',
    routing_key='ikbo-06-22_lyakhov',
    body='Hello exclusive queue!'
)

print("Sent to exclusive queue")
connection.close()
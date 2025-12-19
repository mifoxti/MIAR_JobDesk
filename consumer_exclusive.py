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

def callback(ch, method, properties, body):
    print("Received:", body.decode())

channel.basic_consume(
    queue='ikbo-06-22_lyakhov',
    on_message_callback=callback,
    auto_ack=True
)

print("Waiting for messages...")
channel.start_consuming()
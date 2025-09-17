import pika 

def publish(payload):
    credentials = pika.PlainCredentials('admin', 'admin')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host = 'rabbitmq',
            port = 5672,
            credentials=credentials
        )
    )

    channel = connection.channel()

    channel.queue_declare('infoid', durable=True)
    channel.basic_publish(
        exchange = '',
        routing_key = 'infoid',
        body = payload,

    )
    
    connection.close()
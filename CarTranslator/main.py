import pika
from classes import Translator
import json
import time 


def connect():
    credentials = pika.PlainCredentials('admin', 'admin')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='rabbitmq',
            port=5672,
            credentials=credentials
        )
    )
    channel = connection.channel()
    return connection, channel


def publish_to_db_manager(data):
    connection, channel = connect()
    channel.queue_declare(queue='db_manager', durable=True)
    message = json.dumps(data, ensure_ascii=False)

    channel.basic_publish(
        exchange='',
        routing_key='db_manager',
        body=message.encode('utf-8'),
        properties=pika.BasicProperties(
            delivery_mode=2 
        )
    )
    connection.close()


def worker(ch, method, properties, body):
    translator = Translator()
    data_rabbit = body.decode()
    data_dict = json.loads(data_rabbit)
    data = translator.translator(data_dict)
    publish_to_db_manager(data)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def consumer():
    connection, channel = connect()
    channel.queue_declare(queue='translate', durable=True)
    channel.basic_consume(
        queue='translate',
        on_message_callback=worker,
        auto_ack=False
    )
    try:
        channel.start_consuming()
    except Exception as e:
        print(f"Error {e}")

if __name__ == '__main__':
    time.sleep(60)
    consumer()
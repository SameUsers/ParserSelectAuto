import pika
from classes import CarDetail
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


def publish_to_translate(data):
    connection, channel = connect()
    channel.queue_declare(queue='translate', durable=True)

    message = json.dumps(data, ensure_ascii=False)

    channel.basic_publish(
        exchange='',
        routing_key='translate',
        body=message.encode('utf-8'),
        properties=pika.BasicProperties(
            delivery_mode=2 
        )
    )
    connection.close()


def worker(ch, method, properties, body):
    car_detail_parser = CarDetail()
    infoid = body.decode()
    data = car_detail_parser.get_car_detaile(infoid)
    publish_to_translate(data)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def consumer():
    connection, channel = connect()
    channel.queue_declare(queue='infoid', durable=True)
    channel.basic_consume(
        queue='infoid',
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
import pathlib
import pickle
import pika

import configparser
from mongoengine import connect


def sending():
    file_config = pathlib.Path(__file__).parent.parent.joinpath('config.ini')
    config = configparser.ConfigParser()
    config.read(file_config)

    mongo_user = config.get("DB", "user")
    mongo_pass = config.get("DB", "pass")
    domain = config.get("DB", "domain")
    db_name = config.get("DB", "db_name")

    connect(
        host=f"mongodb+srv://{mongo_user}:{mongo_pass}@{domain}/{db_name}?retryWrites=true&w=majority", ssl=True)

    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672,
                                                                   credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='sending_queue', durable=True)

    def callback(ch, method, properties, body):
        message = pickle.loads(body)
        print(f"[+] Sending to: {message.fullname} <{message.email}>")
        message.done = True
        message.save()

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='sending_queue',
                          on_message_callback=callback, auto_ack=True)
    print('[*] Waiting for messages. To exit CTRL+C')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
        print("Interrupted")


if __name__ == '__main__':
    sending()
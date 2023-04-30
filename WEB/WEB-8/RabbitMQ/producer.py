import pathlib

from models import Contact
import faker
import configparser
import pika
from mongoengine import connect
import pickle


def main():
    file_config = pathlib.Path(__file__).parent.parent.joinpath('config.ini')
    config = configparser.ConfigParser()
    config.read(file_config)

    mongo_user = config.get("DB", "user")
    mongo_pass = config.get("DB", "pass")
    domain = config.get("DB", "domain")
    db_name = config.get("DB", "db_name")

    connect(
        host=f"mongodb+srv://{mongo_user}:{mongo_pass}@{domain}/{db_name}?retryWrites=true&w=majority", ssl=True)

    fake_data = faker.Faker()
    recipients = []

    for _ in range(5):
        recipient = Contact(fullname=fake_data.name(), email=fake_data.email())
        recipient.save()
        recipients.append(recipient)

    credentials = pika.PlainCredentials('guest', 'guest')
    with pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials)) as connection:
        channel = connection.channel()
        channel.queue_declare(queue='sending_queue', durable=True)

        for recipient in recipients:
            channel.basic_publish(
                exchange='', routing_key='sending_queue', body=pickle.dumps(recipient))


if __name__ == '__main__':
    main()
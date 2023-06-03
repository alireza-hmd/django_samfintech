import json
import redis
import csv
from kafka import KafkaProducer

REDIS_CONTAINER = 'redis_redis_1'
r = redis.Redis(host='localhost', port=6379, db=0)


def publish_message(producer_instance, topic_name, value):
    try:
        producer_instance.send(topic_name, value=value)
        producer_instance.flush()
    except Exception as ex:
        print('Exception in publishing message:', str(ex))


def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _producer


with open('../../price_data.csv') as data_file:
    stocks_data = csv.reader(data_file, delimiter=',')
    producer = connect_kafka_producer()
    topic = 'main_topic'
    for row in stocks_data:
        publish_message(producer, topic, row)

from confluent_kafka import Producer
import uuid
import json
import logging
from utils.tfl_api import fetch_tfl_arrivals

KAFKA_CONFIG = {
    'bootstrap.servers': 'kafka:29092',
    'client.id': 'airflow-producer',
    'message.max.bytes': 5242880,
    'compression.type': 'lz4'
}
TOPIC_NAME = 'tfl_arrivals'


def transform_record(record):
    return {
        'id': str(uuid.uuid4()),
        'tfl_id': record['id'],
        'mode_name': record['modeName'],
        'station_name': record['stationName'],
        'platform_name': record['platformName'],
        'towards': record['towards'],
        'timestamp': record['timestamp'],
        'time_to_station': record['timeToStation'],
        'expected_arrival': record['expectedArrival']
    }

def produce_to_kafka():
    producer = Producer(KAFKA_CONFIG)

    def delivery_report(err, msg):
        if err:
            logging.error(f"Delivery failed: {err}")
        else:
            logging.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    try:
        arrivals = fetch_tfl_arrivals()
        for record in arrivals:
            transformed = transform_record(record)
            producer.produce(
                topic=TOPIC_NAME,
                key=transformed['id'],
                value=json.dumps(transformed),
                callback=delivery_report
            )
            producer.poll(0)
        producer.flush()
    except Exception as e:
        logging.error(f"Kafka production failed: {e}")
        raise

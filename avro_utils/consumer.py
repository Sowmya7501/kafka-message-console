import json
import fastavro
from fastavro.schema import load_schema
from kafka import KafkaConsumer
from io import BytesIO
import argparse

def decode_avro_message(schema_file, avro_message):
    # Load the Avro schema
    schema = load_schema(schema_file)

    # Decode the Avro message
    bytes_reader = BytesIO(avro_message)
    reader = fastavro.reader(bytes_reader, schema)
    message = next(reader)

    return message

def avro_consume(brokers, topic, schema_file):
    # Configure the Kafka consumer
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=brokers,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
    )

    try:
        # Consume messages from the Kafka topic
        for message in consumer:
            avro_message = message.value
            decoded_message = decode_avro_message(schema_file, avro_message)
            print(json.dumps(decoded_message, indent=2))
    except KeyboardInterrupt:
        print("Interrupted Exciting...")

"""
def parse_arguments():
    parser = argparse.ArgumentParser(description='Enter the details')
    parser.add_argument('--brokers', type=str, help='The Kafka broker address')
    parser.add_argument('--schema', type=str, help='File descriptor path')
    # parser.add_argument('--help', type=str, help='Help for produce')
    parser.add_argument('--topic', type=str, help='Destination Kafka topic')
    return parser.parse_args()

if '__main__' == __name__:
    args = parse_arguments()
    kafka_brokers = args.brokers
    schema_file = args.schema
    kafka_topic = args.topic

    consume_from_kafka(kafka_brokers, kafka_topic, schema_file)
"""
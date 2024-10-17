import json
import fastavro
from fastavro.schema import load_schema
from kafka import KafkaProducer
from io import BytesIO
import argparse

def generate_avro_message(schema_file, message_data):
    # Load the Avro schema
    schema = load_schema(schema_file)

    # Validate and encode the message data
    bytes_writer = BytesIO()
    fastavro.writer(bytes_writer, schema, [message_data])
    avro_message = bytes_writer.getvalue()

    return avro_message

def avro_produce(brokers, topic, schema_file):
    # Configure the Kafka producer
    producer = KafkaProducer(bootstrap_servers=brokers)

    try:
        while True:
            # Get the message data
            message_data_str = input("Enter the message in JSON format (or q to quit): ")
            if message_data_str == 'q':
                break

            # Parse the JSON string into a dictionary
            try:
                message_data = json.loads(message_data_str)
            except json.JSONDecodeError as e:
                print(f"Invalid JSON format: {e}")
                continue

            # Generate the Avro message
            avro_message = generate_avro_message(schema_file, message_data)
            # Produce the message to the Kafka topic
            future = producer.send(topic, value=avro_message)

            # Block until a single message is sent (or timeout)
            result = future.get(timeout=10)
            print(f"Message delivered to {result.topic} [{result.partition}]")
    except KeyboardInterrupt:
        print("Interrupted Exciting...")

    # Close the producer
    producer.close()

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
    
    Example message data
    message_data = {
        "name": "John Doe",
        "age": 30,
        "email": "john.doe@example.com"
    }
    
    # Generate the Avro message
    # avro_message = generate_avro_message(schema_file, message_data)

    # Produce the Avro message to Kafka
    produce_to_kafka(kafka_brokers, kafka_topic, schema_file)
    """
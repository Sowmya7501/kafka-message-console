from kafka import KafkaProducer
import json
import argparse
from google.protobuf import descriptor_pb2, descriptor_pool, message_factory, json_format
import os

def load_message_descriptor(fd_path, msg_name):
    # Read the file descriptor
    if not os.path.exists(fd_path):
        raise FileNotFoundError(f"File not found: {fd_path}")
    
    with open(fd_path, 'rb') as f:
        file_content = f.read()

    # Unmarshal the file descriptor set
    file_set = descriptor_pb2.FileDescriptorSet()
    file_set.ParseFromString(file_content)

    # Create a descriptor pool and add the file descriptors
    pool = descriptor_pool.DescriptorPool()
    for fd_proto in file_set.file:
        pool.Add(fd_proto)

    # Find the message descriptor
    try:
        message_descriptor = pool.FindMessageTypeByName(msg_name)
        return message_descriptor
    except KeyError:
        raise ValueError(f"Unable to find message named {msg_name} in file descriptor")

def send_message_to_kafka(user_input, msg_descriptor, producer, kafka_topic):
    # Create a message factory
    factory = message_factory.MessageFactory()

    # Get the message class from the descriptor
    message_class = factory.GetPrototype(msg_descriptor)

    # Create an instance of the message
    dymsg = message_class()

    # Unmarshal JSON string into the message
    try:
        json_format.Parse(user_input, dymsg)
    except json_format.ParseError as e:
        print(f"Error parsing JSON: {e}")
        return e

    # Serialize the message to bytes
    message_bytes = dymsg.SerializeToString()

    # Send the message to Kafka
    try:
        producer.send(topic = kafka_topic, value = message_bytes)
    except Exception as e:
        return e

def protobuf_produce(brokers, descriptor, name, topic):
    producer = KafkaProducer(bootstrap_servers=brokers)
    message_descriptor = load_message_descriptor(descriptor, name)
    try:
        while True:
            user_input = input("Enter the message in JSON format (or q to quit): ")
            if user_input == 'q':
                break
            send_message_to_kafka(user_input, message_descriptor, producer, topic)
    except KeyboardInterrupt:
        print("Interrupted")
    finally:
        producer.close()

# def parse_arguments():
#     parser = argparse.ArgumentParser(description='Enter the details')
#     parser.add_argument('--brokers', type=str, help='The Kafka broker address')
#     parser.add_argument('--descriptor', type=str, help='File descriptor path')
#     # parser.add_argument('--help', type=str, help='Help for produce')
#     parser.add_argument('--name', type=str, help='Fully qualified Proto message name')
#     parser.add_argument('--topic', type=str, help='Destination Kafka topic')
#     return parser.parse_args()

# if '__main__' == __name__:
#     args = parse_arguments()
#     kafka_brokers = args.brokers
#     descriptor_file = args.descriptor
#     message_name = args.name
#     kafka_topic = args.topic

#     produce(kafka_brokers, descriptor_file, message_name, kafka_topic)
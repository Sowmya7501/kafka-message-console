import argparse
import subprocess

from avro_utils import avro_produce, avro_consume
from protobuf_utils import generate_descriptor, protobuf_consume, protobuf_produce, protobuf_validate_message

def parse_arguments():
    parser = argparse.ArgumentParser(description='Kafka Producer/Consumer')
    parser.add_argument('--format', type=str, required=False, help='The message format (avro or protobuf)')
    parser.add_argument('--brokers', type=str, required=False, help='The Kafka broker address')
    parser.add_argument('--descriptor', type=str, required=False, help='File descriptor path')
    parser.add_argument('--schema', type=str, required=False, help='Avro schema path')
    parser.add_argument('--name', type=str, required=False, help='Fully qualified Proto message name')
    parser.add_argument('--topic', type=str, required=False, help='Kafka topic')
    parser.add_argument('--mode', type=str, required=True, choices=['produce','consume','validate','generate'], help='Mode: produce or consume or validate or generate')
    parser.add_argument('--proto',type=str, required=False, help='Path to the .proto file')
    parser.add_argument('--out', type=str, required=False, help='Path to the output descriptor file with the name of the file')
    return parser.parse_args()

def check_options(args):
    if args.mode == 'produce' or args.mode == 'consume':
        if args.format is None:
            raise ValueError("The --format option is required for produce/consume mode")
        if args.brokers is None:
            raise ValueError("The --brokers option is required for produce/consume mode")
        if args.topic is None:
            raise ValueError("The --topic option is required for produce/consume mode")
        if args.name is None:
            raise ValueError("The --name option is required for produce/consume mode")
        if args.format == 'protobuf' and args.descriptor is None:
            raise ValueError("The --descriptor option is required for protobuf produce/consume mode")
        if args.format == 'avro' and args.schema is None:
            raise ValueError("The --schema option is required for avro produce/consume mode")
    elif args.mode == 'validate' and args.format == 'protobuf':
        if args.descriptor is None:
            raise ValueError("The --descriptor option is required for validate mode")
        if args.name is None:
            raise ValueError("The --name option is required for validate mode")
    elif args.mode == 'generate' and args.format == 'protobuf':
        if args.proto is None:
            raise ValueError("The --proto option is required for generate mode")
        if args.out is None:
            raise ValueError("The --out option is required for generate mode")

def main():
    args = parse_arguments()
    if args.format == 'protobuf':
        if args.mode == 'produce':
            protobuf_produce(args.brokers, args.descriptor, args.name, args.topic)
        elif args.mode == 'consume':
            protobuf_consume(args.brokers, args.descriptor, args.name, args.topic)
        elif args.mode == 'validate':
            protobuf_validate_message(args.descriptor, args.name)
        elif args.mode == 'generate':
            generate_descriptor(args.proto, args.out)
    elif args.format == 'avro':
        if args.mode == 'produce':
            avro_produce(args.brokers, args.topic, args.schema)
        elif args.mode == 'consume':
            avro_consume(args.brokers, args.topic, args.schema)

if __name__ == '__main__':
    main()
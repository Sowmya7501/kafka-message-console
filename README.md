# kafka-message-console

This tool provides functionalities to produce and consume messages in both Protobuf and Avro formats to/from Kafka, as well as to validate and generate Protobuf descriptors.

## Features
- Produce Protobuf messages to Kafka using JSON input
- Consume Protobuf messages from Kafka and display them in JSON format
- Validate Protobuf messages against a schema
- Generate Protobuf descriptor files from `.proto` files
- Produce Avro messages to Kafka using JSON input
- Consume Avro messages from Kafka and display them in JSON format

## Requirements
- Python 3.x

## Installation

1. Clone the repository

2. Create and activate a virtual environment:
    ```bash
    python -m venv myenv
    # On Windows
    myenv\Scripts\activate
    # On macOS/Linux
    source myenv/bin/activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
```bash
python kafka_message_tool.py [flags]

Flags:
    --format: Specifies the message format. It can be either avro or protobuf. This flag is required for produce and consume modes.
    --brokers: Specifies the Kafka broker address. This flag is required for produce and consume modes.
    --descriptor: Specifies the path to the Protobuf descriptor file. This flag is required for protobuf produce, consume, and validate modes.
    --schema: Specifies the path to the Avro schema file. This flag is required for avro produce and consume modes.
    --name: Specifies the fully qualified Protobuf message name. This flag is required for protobuf produce, consume, and validate modes.
    --topic: Specifies the Kafka topic. This flag is required for produce and consume modes.
    --mode: Specifies the mode of operation. It can be one of the following:
        produce: Produce messages to Kafka.
        consume: Consume messages from Kafka.
        validate: Validate Protobuf messages against the descriptor.
        generate: Generate Protobuf descriptor files from .proto files.
    --proto: Specifies the path to the .proto file. This flag is required for protobuf generate mode.
    --out: Specifies the path to the output descriptor file with the name of the file. This flag is required for protobuf generate mode.
```

- Note: Refer the example scripts to know more

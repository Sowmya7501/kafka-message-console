### Protobuf

- Generate desc file from proto
```bash
python kafka_message_tool.py --mode generate --format protobuf --proto ./examples/example.proto --out example.desc
```

- Command to run a producer
```bash
python kafka_message_tool.py --mode produce --format protobuf --brokers kafka_broker --descriptor ./examples/example.desc --name ExampleData --topic kafka_topic
```

- Command to run consumer
```bash
python kafka_message_tool.py --mode consume --format protobuf --brokers kafka_broker --descriptor ./examples/example.desc --name ExampleData --topic kafka_topic
```

- Command to validate message
```bash
python kafka_message_tool.py --mode validate --format protobuf --descriptor ./examples/example.desc --name ExampleData
```

### Avro
- Produce avro message to kafka
```bash
python kafka_message_tool.py --mode produce --format avro --brokers kafka_broker --schema example.avsc --topic kafka_topic
```

- Consume avro message from kafka
```bash
python kafka_message_tool.py --mode consume --format avro --brokers kafka_broker --schema example.avsc --topic kafka_topic
```
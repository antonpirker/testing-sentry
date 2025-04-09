# Kafka Hello World Example

This is a minimal example of using Apache Kafka with the confluent-kafka Python library.

## Prerequisites

1. Python 3.13+ (as specified in pyproject.toml)
2. A running Kafka broker on localhost:9092
3. Required Python packages listed in pyproject.toml

## Setup Kafka (if not already running)

The simplest way to get Kafka running locally is using Docker:

```bash
# Pull and run Kafka using Docker
./run-kafka.sh
```

## Files in this Example

- `producer.py`: Standalone producer that sends 5 messages
- `consumer.py`: Standalone consumer that listens for messages indefinitely
- `run-*.sh`: Script to set up environment and run examples

## Running the Examples

In one terminal, run the consumer:
```bash
./run-consumer.sh
```

In another terminal, run the producer:
```bash
./run-producer.sh
```

The producer will send 5 messages, and the consumer will receive and print them.

## Notes on Kafka Configuration

- Both producer and consumer are configured to connect to `localhost:9092`
- The consumer is configured to read from the earliest offset (`auto.offset.reset='earliest'`)
- The consumer uses the group ID `hello-world-consumer`

You may need to adjust these settings based on your Kafka setup.

## Troubleshooting

1. **Connection refused**: Make sure Kafka is running and accessible at localhost:9092
2. **Topic not found**: Kafka typically creates topics automatically, but if this doesn't happen, you may need to create the topic manually:

   ```bash
   # If using Docker:
   docker exec -it [kafka-container-id] kafka-topics.sh \
     --create --topic hello-world-topic \
     --bootstrap-server localhost:9092 \
     --partitions 1 \
     --replication-factor 1
   ```

3. **No messages received**: Check if the producer succeeded in sending messages. The consumer is configured to read from the beginning of the topic, so it should read any existing messages.

from confluent_kafka import Consumer
import json
import signal
import sys

# Topic to be used
TOPIC_NAME = "hello-world-topic"

# Flag to control the consumer loop
running = True


def signal_handler(sig, frame):
    """Handle interrupt signals"""
    global running
    print("Stopping consumer...")
    running = False


def main():
    """Simple Kafka consumer"""
    print("Kafka Consumer Example")
    print("---------------------")

    # Set up signal handling for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)

    # Consumer configuration
    consumer_conf = {
        'bootstrap.servers': 'localhost:9092',  # Update with your Kafka broker address
        'group.id': 'hello-world-consumer',
        'auto.offset.reset': 'earliest'  # Start from the beginning of the topic
    }

    # Create Consumer instance
    consumer = Consumer(consumer_conf)

    try:
        # Subscribe to topic
        consumer.subscribe([TOPIC_NAME])
        print(f"Subscribed to topic: {TOPIC_NAME}")
        print("Waiting for messages... (Press Ctrl+C to exit)")

        # Process messages until interrupted
        while running:
            # Poll for messages with a 1-second timeout
            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            # Process the received message
            try:
                value = json.loads(msg.value().decode('utf-8'))
                print("\nReceived message:")
                print(f"  Value: {value}")
                print(f"  Key: {msg.key().decode('utf-8') if msg.key() else 'None'}")
                print(f"  Topic: {msg.topic()}, Partition: {msg.partition()}, Offset: {msg.offset()}")
            except Exception as e:
                print(f"Error processing message: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        # Close down consumer
        consumer.close()
        print("\nConsumer closed")


if __name__ == '__main__':
    main()

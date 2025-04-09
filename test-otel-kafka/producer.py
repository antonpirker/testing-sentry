from confluent_kafka import Producer
import socket
import json
import time
import signal
import sys

# Topic to be used
TOPIC_NAME = "hello-world-topic"

# Flag to control the producer loop
running = True


def signal_handler(sig, frame):
    """Handle interrupt signals"""
    global running
    print("Stopping producer...")
    running = False


def delivery_callback(err, msg):
    """Callback invoked after message delivery (success or failure)"""
    if err:
        print(f"ERROR: Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")


def main():
    """Simple Kafka producer"""
    print("Kafka Producer Example")
    print("---------------------")

    # Set up signal handling for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)

    # Producer configuration
    producer_conf = {
        'bootstrap.servers': 'localhost:9092',  # Update with your Kafka broker address
        'client.id': socket.gethostname()
    }

    # Create Producer instance
    producer = Producer(producer_conf)

    try:
        message_count = 0

        # Loop to send messages until interrupted
        while running and message_count < 5:
            # Create message
            message = {
                "message": f"Hello, Kafka! Message #{message_count+1}",
                "timestamp": time.time()
            }

            # Produce message to topic
            producer.produce(
                TOPIC_NAME,
                key=f"key-{message_count}",
                value=json.dumps(message),
                callback=delivery_callback
            )

            print(f"Message #{message_count+1} queued for delivery")
            message_count += 1

            # Poll for callbacks to be executed
            producer.poll(0)

            # Small delay between messages
            time.sleep(0.5)

        # Wait for any outstanding messages to be delivered
        if message_count > 0:
            print("\nFlushing producer...")
            producer.flush()
            print("All messages delivered!")

    except Exception as e:
        print(f"Error producing message: {e}")
    finally:
        # Always flush before exiting to ensure delivery of all messages
        producer.flush()
        print("Producer closed")


if __name__ == '__main__':
    main()

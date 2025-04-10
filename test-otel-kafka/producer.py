import json
import signal
import socket
import time

from otel_config import configure_opentelemetry_producer

from confluent_kafka import Producer


# Initialize OpenTelemetry
tracer = configure_opentelemetry_producer()

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
    print("Kafka Producer Example with OpenTelemetry Instrumentation")
    print("--------------------------------------------------------")

    # Set up signal handling for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)

    # Producer configuration
    producer_conf = {
        'bootstrap.servers': 'localhost:9092',  # Connect to Kafka on localhost
        'client.id': socket.gethostname()
    }

    # Create Producer instance
    producer = Producer(producer_conf)

    try:
        message_count = 0

        # Loop to send messages until interrupted
        while running and message_count < 5:
            # Create a span for producing each message
            with tracer.start_as_current_span(f"produce_message_{message_count+1}") as span:
                # Add attributes to the span
                span.set_attribute("message.count", message_count + 1)

                # Create message
                message = {
                    "message": f"Hello, Kafka! Message #{message_count+1}",
                    "timestamp": time.time()
                }

                # Add more context to span
                span.set_attribute("message.content", message["message"])

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
                time.sleep(0.2)

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

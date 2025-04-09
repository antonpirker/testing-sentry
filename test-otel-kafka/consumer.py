from confluent_kafka import Consumer
import json
import signal
import sys
from opentelemetry import trace
from otel_config import configure_opentelemetry_consumer

# Initialize OpenTelemetry
tracer = configure_opentelemetry_consumer()

# Topic to be used
TOPIC_NAME = "hello-world-topic"

# Flag to control the consumer loop
running = True


def signal_handler(sig, frame):
    """Handle interrupt signals"""
    global running
    print("Stopping consumer...")
    running = False


def process_message(msg):
    """Process a message with OpenTelemetry instrumentation"""
    # Start a new span for message processing
    with tracer.start_as_current_span("process_message") as span:
        try:
            # Extract message value and add context to span
            value = json.loads(msg.value().decode('utf-8'))
            key = msg.key().decode('utf-8') if msg.key() else 'None'

            # Add attributes to span
            span.set_attribute("message.key", key)
            span.set_attribute("message.topic", msg.topic())
            span.set_attribute("message.partition", msg.partition())
            span.set_attribute("message.offset", msg.offset())
            span.set_attribute("message.content", str(value))

            # Print message details
            print("\nReceived message:")
            print(f"  Value: {value}")
            print(f"  Key: {key}")
            print(f"  Topic: {msg.topic()}, Partition: {msg.partition()}, Offset: {msg.offset()}")

            # Return the processed value
            return value
        except Exception as e:
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
            print(f"Error processing message: {e}")
            return None


def main():
    """Simple Kafka consumer with OpenTelemetry instrumentation"""
    print("Kafka Consumer Example with OpenTelemetry Instrumentation")
    print("--------------------------------------------------------")

    # Set up signal handling for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)

    # Consumer configuration
    consumer_conf = {
        'bootstrap.servers': 'localhost:9092',  # Connect to Kafka on localhost
        'group.id': 'hello-world-consumer',
        'auto.offset.reset': 'earliest'  # Start from the beginning of the topic
    }

    # Create Consumer instance
    consumer = Consumer(consumer_conf)

    try:
        # Create a span for the subscription process
        with tracer.start_as_current_span("subscribe_to_topic") as span:
            span.set_attribute("kafka.topic", TOPIC_NAME)
            # Subscribe to topic
            consumer.subscribe([TOPIC_NAME])
            print(f"Subscribed to topic: {TOPIC_NAME}")
            print("Waiting for messages... (Press Ctrl+C to exit)")

        # Process messages until interrupted
        with tracer.start_as_current_span("consume_messages") as consume_span:
            consume_span.set_attribute("kafka.topic", TOPIC_NAME)
            while running:
                # Poll for messages with a 1-second timeout
                msg = consumer.poll(1.0)

                if msg is None:
                    continue

                if msg.error():
                    error_msg = f"Consumer error: {msg.error()}"
                    consume_span.add_event("error", {"error.message": error_msg})
                    print(error_msg)
                    continue

                # Process the received message
                process_message(msg)

    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        # Close down consumer
        consumer.close()
        print("\nConsumer closed")


if __name__ == '__main__':
    main()

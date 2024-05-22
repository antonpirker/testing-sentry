import os
import time

from datetime import datetime, timezone

import sentry_sdk


def main():
    sentry_sdk.init(
        dsn=os.environ["SENTRY_DSN"],
        enable_tracing=True,
        debug=True,
    )

    # The message you want to send to the queue
    queue = "messages"
    message = "Hello World!"
    message_id = "abc123"

    ### PUBLISH

    # Create the span
    with sentry_sdk.start_transaction(op="function", name="queue_producer_transaction") as transaction:
        with sentry_sdk.start_span(op="queue.publish", description="queue_producer") as span:    
            # Set span data
            span.set_data("messaging.message.id", message_id)
            span.set_data("messaging.destination.name", queue)
            span.set_data("messaging.message.body.size", len(message.encode("utf-8")))
            
            ts = int(datetime.now(timezone.utc).timestamp())

            headers = {
                "sentry-trace": sentry_sdk.get_traceparent(),
                "baggage": sentry_sdk.get_baggage()            
            }
        

            # Publish the message to the queue (including trace information and current time stamp)
            # connection.publish(
            #     queue=queue,
            #     body=message,
            #     timestamp=now,
            #     headers = {
            #         "sentry-trace": sentry_sdk.get_traceparent()
            #         "baggage": sentry_sdk.get_baggage()            
            #     },
            # )


    time.sleep(0.3)


    ### CONSUME
    message = {
        "message_id": "abc123",
        "body": "Hello World!",
        "timestamp": ts,
        "headers": headers,
    }

    # Calculate latency (optional, but valuable)
    now = datetime.now(timezone.utc)
    message_time = datetime.fromtimestamp(message["timestamp"], timezone.utc)
    latency =  now - message_time

    # Continue the trace started in the producer
    transaction = sentry_sdk.continue_trace(
        message["headers"],
        op="function",
        name="queue_consumer_transaction",
    )
    with sentry_sdk.start_transaction(transaction):
        # Create the span
        with sentry_sdk.start_span(op="queue.process", description="queue_consumer") as span:
            # Set span data
            span.set_data("messaging.message.id", message["message_id"])
            span.set_data("messaging.destination.name", queue)
            span.set_data("messaging.message.body.size", message["body"])
            span.set_data("messaging.message.receive.latency", latency.total_seconds()*1000)
            span.set_data("messaging.message.retry.count", 0)
            
            try:
                # Process the message
                # process_message(message)
                pass
            except Exception:
                span.set_status("internal_error")            


if __name__ == "__main__":
    main()

import os
import signal
import time

import sentry_sdk


def signal_handler(sig, frame):
    print("SIGINT received")
    sentry_sdk.capture_message("SIGINT received")

    with sentry_sdk.start_transaction(name="xxxpython312") as transaction:
        transaction.set_status("ok")
        for x in range(10):
            with sentry_sdk.start_span(description=f"xxxchild{x} descriptions") as span:
                span.set_data("x", x)

    import sys
    sys.exit(0)


def main():
    sentry_settings = {
        "dsn": os.getenv("SENTRY_DSN", None),
        "environment": os.getenv("ENV", "local"),
        "traces_sample_rate": 1.0,
        # "send_default_pii": True,
        "debug": True,
        # "integrations": [],
    }
    print(f"Sentry Settings: {sentry_settings}")

    sentry_sdk.init(**sentry_settings)

    signal.signal(signal.SIGINT, signal_handler)
    
    with sentry_sdk.start_transaction(name="python312") as transaction:
        transaction.set_status("ok")
        for x in range(10):
            with sentry_sdk.start_span(description=f"child{x} descriptions") as span:
                span.set_data("x", x)

    time.sleep(10)


if __name__ == "__main__":
    main()

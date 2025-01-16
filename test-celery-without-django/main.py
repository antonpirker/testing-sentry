import os

import sentry_sdk

from tasks import message


def main():
    # Initializing Sentry SDK in our process
    # This is not the process Celery runs in.
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN", None),
        traces_sample_rate=1.0,
        debug=True,
    )

    # Enqueueing a task to be processed by Celery
    with sentry_sdk.start_transaction(name="calling-a-celery-task"):
        result = message.apply_async(
            args=("This should be connected.", ),
        )
        print(f"Task ID 1: {result.id}")

        result = message.apply_async(
            args=("This should NOT be connected.", ),
            headers={"sentry-propagate-traces": False},
        )
        print(f"Task ID 2: {result.id}")

if __name__ == "__main__":
    main()

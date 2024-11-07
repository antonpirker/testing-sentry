import os

import sentry_sdk

from tasks import add


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
        result = add.delay(4, 4)
        print(f"Task ID: {result.id}")


if __name__ == "__main__":
    main()

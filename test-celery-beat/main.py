import os
import sentry_sdk

from tasks import task_a, task_b


def main():
    sentry_settings = {
        "dsn": os.getenv("SENTRY_DSN", None),
        "environment": os.getenv("ENV", "local.main"),
        "release": "0.0.0",        
        "traces_sample_rate": 1.0,
        "send_default_pii": True,
        "debug": True,
    }
    print(f"Sentry Settings: {sentry_settings}")
    sentry_sdk.init(**sentry_settings)

    with sentry_sdk.start_transaction(op="function", name="celery-task-started-from-transaction"):
        task_a.delay("Task A from main (via delay)")
        task_b.apply_async(("Task B from main (via apply_async)", ))


if __name__ == "__main__":
    main()
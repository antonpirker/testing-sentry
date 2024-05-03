import datetime

import os

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration


from tasks import task_a, task_b, before_send_transaction

exclude_beat_tasks=[]

def main():
    sentry_settings = {
        "dsn": os.getenv("SENTRY_DSN", None),
        "environment": os.getenv("ENV", "local"),
        "traces_sample_rate": 1.0,
        "send_default_pii": True,
        "debug": True,
        "before_send_transaction": before_send_transaction,
        "integrations": [
            CeleryIntegration(monitor_beat_tasks=True, exclude_beat_tasks=exclude_beat_tasks),
        ],
    }
    print(f"Sentry Settings: {sentry_settings}")

    sentry_sdk.init(**sentry_settings)

    with sentry_sdk.start_transaction(op="function", name="celery-propagate-traces"):
        # import ipdb; ipdb.set_trace()
        task_a.delay("Task A msg 2")
        # task_b.apply_async(("Task B msg", ))
        # task_b.apply_async(("Task B msg 2", ), headers={"sentry-propagate-traces": False})


if __name__ == "__main__":
    main()
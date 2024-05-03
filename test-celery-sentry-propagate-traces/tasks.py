import os 

from celery import Celery, signals

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration


app = Celery("tasks", broker='redis://localhost:6379/0')

def before_send_transaction(event, hint):
    print(event)

exclude_beat_tasks = []

@signals.celeryd_init.connect
def concect_sentry(**kwargs):
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN", None),
        integrations=[
            CeleryIntegration(monitor_beat_tasks=True, exclude_beat_tasks=exclude_beat_tasks),
        ],
        environment="dev.celery",
        release="0.0.0",
        traces_sample_rate=1,
        debug=True,
        before_send_transaction=before_send_transaction,
    )


@app.task
def task_a(msg):
    print("[task-a] That's my message to the world: %s" % msg)
    import time
    time.sleep(0.05)
    # raise Exception("Something went wrong in the world")


@app.task
def task_b(msg):
    print("[task-b] Hello there %s" % msg)
    raise Exception("Oh no! Abort! Alarm alarm!")

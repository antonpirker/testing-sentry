import os 

from celery import Celery, signals

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration


app = Celery(
    "tasks", 
    broker="redis://localhost:6379/0",
    result_backend="redis://localhost:6379/1",
)


@signals.celeryd_init.connect
def concect_sentry(**kwargs):
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN", None),
        traces_sample_rate=1,
        debug=True,
        integrations=[
            # CeleryIntegration(),
        ],
    )


@app.task
def task_a(msg):
    print("[task-a] That's my message to the world: %s" % msg)
    raise Exception("Something went wrong in the world")


@app.task
def task_b(msg):
    return "[task-b] Hello there %s" % msg

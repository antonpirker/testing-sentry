import os 

from celery import Celery, signals

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration


app = Celery("tasks", broker='redis://localhost:6379/0')


@signals.celeryd_init.connect
def concect_sentry(**kwargs):
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN", None),
        integrations=[
            CeleryIntegration(),
        ],
        environment="dev.celery",
        release="0.0.0",
        traces_sample_rate=1,
        debug=True,
    )


@app.task
def task_a(msg):
    print("[task-a] That's my message to the world: %s" % msg)
    raise Exception("Something went wrong in the world")


@app.task
def task_b(msg):
    print("[task-b] Hello there %s" % msg)
    raise Exception("Oh no! Abort! Alarm alarm!")

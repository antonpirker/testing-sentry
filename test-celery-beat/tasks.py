import os
import time
import random

from celery import Celery, signals
from celery.schedules import crontab

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration


app = Celery("tasks", broker='redis://localhost:6379/0')
app.conf.beat_schedule = {
    'task_a_beat': {
        'task': 'tasks.task_a',
        'schedule': crontab(minute='*/1'),
        'args': ('Task A from beat',),
    },
    # 'task_b_beat': {
    #     'task': 'tasks.task_b',
    #     'schedule': crontab(minute='*/1'),
    #     'args': ('Task B from beat',),
    # },
}
app.conf.timezone = 'UTC'

def before_send_transaction(event, hint):
    print(event)
    return event

exclude_beat_tasks=[]

@signals.beat_init.connect   # omit this line if you're running beat directly within your worker process
@signals.celeryd_init.connect
def connect_sentry(**kwargs):
    sentry_settings = {
        "dsn": os.getenv("SENTRY_DSN", None),
        "environment": os.getenv("ENV", "local.celery"),
        "release": "0.0.0",
        "traces_sample_rate": 1.0,
        "send_default_pii": True,
        "debug": True,
        "integrations": [
            CeleryIntegration(monitor_beat_tasks=True, exclude_beat_tasks=exclude_beat_tasks),
        ],
        "before_send_transaction": before_send_transaction,
    }
    print(f"Sentry Settings: {sentry_settings}")
    sentry_sdk.init(**sentry_settings)


@app.task
def task_a(msg):
    print("[task-a] That's my message to the world: %s" % msg)
    task_b.delay("Task B started from Task A")


@app.task
def task_b(msg):
    print("[task-b] Hello there %s" % msg)
    # time.sleep(10)
    raise Exception("Oh no! Abort! Alarm alarm!")

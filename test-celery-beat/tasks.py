import os 
import time
import random

from celery import Celery, signals
from celery.schedules import crontab

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration


app = Celery("tasks", broker='redis://localhost:6379/0')
app.conf.beat_schedule = {
    'task_propagate_6': {
        'task': 'tasks.task_a',
        'schedule': crontab(minute='*/1'),
        'args': ('Task A from beat',),
    },
    'task_b': {
        'task': 'tasks.task_b',
        'schedule': crontab(minute='*/1'),
        'args': ('Task B from beat',),
    },
}
app.conf.timezone = 'UTC'


# @signals.beat_init.connect   # omit this line if you're running beat directly within your worker process
@signals.celeryd_init.connect
def connect_sentry(**kwargs):
    sentry_settings = {
        "dsn": os.getenv("SENTRY_DSN", None),
        "environment": os.getenv("ENV", "local.celery"),
        "release": "0.0.0",
        "traces_sample_rate": 1.0,
        "send_default_pii": True,
        "debug": True,
        "integrations": [CeleryIntegration(
            monitor_beat_tasks=True, 
            propagate_traces=False, 
        )],
    }
    print(f"Sentry Settings: {sentry_settings}")
    sentry_sdk.init(**sentry_settings)


@app.task
def task_a(msg):
    print("[task-a] That's my message to the world: %s" % msg)
    for _ in range(1):
        with sentry_sdk.start_transaction(op="function", name="trx-with-metrics"):
            for x in range(20000):
                time.sleep(1)
                with sentry_sdk.metrics.timing(key="metric_timing"):
                    sentry_sdk.metrics.incr(
                        key="metric_increment",
                        value=1,
                        tags={
                            "browser": "Firefox",
                            "app_version": "1.0.0"
                        }
                    ) 
                    sentry_sdk.metrics.distribution(
                        key="metric_distribution",
                        value=random.randint(10, 50),
                        unit="millisecond",
                        tags={
                            "page": "/home"
                        }
                    )
                    sentry_sdk.metrics.set(
                        key="metric_set",
                        value="jane",
                        unit="username",
                        tags={
                            "page": "/home"
                        }
                    )
                    sentry_sdk.metrics.gauge(
                        key="metric_gauge",
                        value=random.randint(10, 200),
                        unit="millisecond",
                        tags={
                            "page": "/home"
                        }
                    )


@app.task
def task_b(msg):
    print("[task-b] Hello there %s" % msg)
    # time.sleep(10)
    # raise Exception("Oh no! Abort! Alarm alarm!")

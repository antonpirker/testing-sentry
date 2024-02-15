import os 

from celery import Celery, signals

import django 

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()

app = Celery("tasks", broker='redis://localhost:6379/0')
app.conf.timezone = "Europe/Paris"


@signals.celeryd_init.connect
def connect_sentry(**kwargs):
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN", None),
        environment="dev.celery",
        release="0.0.0",
        traces_sample_rate=1,
        debug=True,
        integrations=[
            CeleryIntegration(monitor_beat_tasks=True), 
        ],
    )


@app.task
def test_task(msg):
    print("[test_task] That's my message to the world: %s" % msg)
    # raise Exception("Something went wrong in the world")


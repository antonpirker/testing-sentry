import os 
from celery import Celery
from celery.signals import celeryd_init
from celery.schedules import crontab
import sentry_sdk
from sentry_sdk.crons.decorator import monitor
from sentry_sdk.integrations.celery import CeleryIntegration

app = Celery(__name__, broker='redis://localhost:6379/0')

@celeryd_init.connect
def init_sentry(**_kwargs):
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN", None),
        environment='development',
        release='unknown',
        integrations=[CeleryIntegration(monitor_beat_tasks=True)],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production,
        traces_sample_rate=1.0,
        debug=True,
    )


@app.task
@monitor(monitor_slug='task_a_redbeat')
def task_a():
    print('Hello World from task_a!')
    task_b.delay()


@app.task
def task_b():
    print('Hello World from task_b!')
    raise Exception("Error in TASK B")


# Redbeat Configuration
app.conf.redbeat_redis_url = 'redis://localhost:6379/1'
app.conf.beat_scheduler = 'redbeat.RedBeatScheduler'
app.conf.beat_schedule = {
    'task_a_redbeat': {
        'task': 'tasks.task_a',
        'schedule': crontab(minute='*/1'),
    },
}
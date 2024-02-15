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
        integrations=[CeleryIntegration()],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production,
        traces_sample_rate=0.005,
        debug=True,
    )


@app.task
@monitor(monitor_slug='my_celery_task')
def my_celery_task():
    print('Hello World from my_celery_task!')


app.conf.redbeat_redis_url = 'redis://localhost:6379/1'
app.conf.beat_scheduler = 'redbeat.RedBeatScheduler'
app.conf.beat_schedule = {
    'my-celery-task': {
        'task': 'tasks.my_celery_task',
        'schedule': crontab(minute='*'),
    },
}
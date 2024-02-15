
from celery import Celery, signals

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration

# 'python' project on Sentry.io
DSN = "https://2c6ef38b3a00490ba49b4677dbef4db6@o447951.ingest.sentry.io/4505239425777664"

app = Celery('tasks', broker='redis://localhost:6379')

@signals.celeryd_init.connect
def connect_sentry(**kwargs):
    print("------------------connected sentry to celery ------------------------")
    sentry_sdk.init(
        dsn=DSN,
        debug=True,
#        traces_sample_rate=1.0,
        integrations=[
            CeleryIntegration(
                propagate_traces=False,
            ),
        ], 
    )


@app.task()
def add_together(a, b):
    some_other_task.delay(1, 2)
    raise Exception("222 Error in celery task")
    return a + b


@app.task()
def some_other_task(a, b):
    raise Exception("222 Another Error in celery task")
    return a + b


import os

from celery import Celery, signals

import sentry_sdk


# Initializing Celery
app = Celery("tasks", broker="redis://localhost:6379/0")


@signals.worker_init.connect  # run for each worker process starting
# @signals.celeryd_init.connect  # run once when Celery deamon starts (before workers are spawned)
def init_sentry(**_kwargs):
    # Initializing Sentry SDK in the Celery worker process
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN", None),
        traces_sample_rate=1.0,
        debug=True,
    )


# Setup Celery Tasks
@app.task
def add(x, y):
    import logging
    logging.warning("In add task")
    return x + y


@app.task
def message(msg):
    import logging
    logging.warning("In msg task(%s)", msg)
    return msg

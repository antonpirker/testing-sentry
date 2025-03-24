import logging
import os
import time

from flask import Flask

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_sdk.init(
    dsn=os.environ["SENTRY_DSN"],
    traces_sample_rate=1.0,
    integrations=[
        LoggingIntegration(
            level=logging.INFO,
            event_level=logging.INFO,#WARNING,
        ),
    ],
    profiles_sample_rate=1.0,
    debug=True,
)


app = Flask(__name__)

logging.info('Flask app initialized')


@sentry_sdk.trace
def fibonacci(n):
    time.sleep(0.01)
    if n < 0:
        print("Incorrect input")
    elif n == 0:
        return 0
    elif n == 1 or n == 2:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)


@app.route("/")
def index():
    logging.info('Flask index route called')
    with sentry_sdk.start_span(name="test"):
        fibonacci(10)
        return {"message": "Hello, World!"}


@app.route('/favicon.ico')
def favicon():
    logging.info('Flask favicon route called')
    return '', 204

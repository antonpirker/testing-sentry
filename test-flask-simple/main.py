import os
from flask import Flask

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
)

import sentry_sdk

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN", None),
    environment=os.getenv("ENV", "local"),
    traces_sample_rate=1.0,
    send_default_pii=True,
    enable_logs=True,
    debug=True,
)


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/err")
def err():
    try:
        1/0
    except Exception as e:
        logger.exception(e)
        raise e

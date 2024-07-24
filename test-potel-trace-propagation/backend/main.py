import os
import random
import time

from flask import Flask, request
import sentry_sdk

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN", None),
    environment="potel",
    release="unknown",
    traces_sample_rate=1.0,
    enable_db_query_source=True,
    db_query_source_threshold_ms=0,
    debug=True,
    _experiments={
        "otel_powered_performance": True
    },
)

app = Flask(__name__)


@app.route("/")
def index():
    print("------")
    print("sentry-trace:")
    print(request.environ.get("HTTP_SENTRY_TRACE"))
    print("baggage:")
    print(request.environ.get("HTTP_BAGGAGE"))
    print("tracestate:")
    print(request.environ.get("HTTP_TRACESTATE"))
    
    return { "content": "Flask (backend)"}
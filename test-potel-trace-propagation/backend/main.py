import os
import random
import time

from flask import Flask
import sentry_sdk

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN", None),
    environment="development",
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
def stream_response():
    num = random.randint(1, 100)
    sentry_sdk.set_tag(f"tag_num", num)

    def generate():
        for _ in range(100):
            yield f"{num}_{_}|"
            if _ % 100 == 0:
                time.sleep(0.1)
                yield "\n"
                print(num)

        1 / 0

    return generate(), {"Content-Type": "text/plain"}

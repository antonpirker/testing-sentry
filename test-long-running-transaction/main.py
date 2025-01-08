import os
import time
from unittest import mock

import sentry_sdk
from sentry_sdk.integrations.wsgi import SentryWsgiMiddleware

from werkzeug.test import Client


def main():
    # we allow transactions to be 0.5 seconds as a maximum
    new_max_duration = 0.5

    with mock.patch.object(
        sentry_sdk.tracing,
        "MAX_TRANSACTION_DURATION_SECONDS",
        new_max_duration,
    ):

        def generate_content():
            # This response will take 1.5 seconds to generate
            for _ in range(15):
                with sentry_sdk.start_span(op="function", name=f"sleep {_}"):
                    time.sleep(0.1)
                    yield "ok"

        def long_running_app(environ, start_response):
            start_response("200 OK", [])
            return generate_content()

        sentry_sdk.init(
            dsn=os.environ["SENTRY_DSN"],
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
        )

        app = SentryWsgiMiddleware(long_running_app)

        client = Client(app)
        response = client.get("/")
        _ = response.get_data()


if __name__ == "__main__":
    main()


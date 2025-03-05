import os

import sentry_sdk


sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN", None),
    traces_sample_rate=1.0,
    debug=True,
)

try:
    try:
        raise ExceptionGroup("group", [ValueError("child1"), ValueError("child2")])
    finally:
        raise TypeError("bar")
except BaseException:
    sentry_sdk.capture_exception()

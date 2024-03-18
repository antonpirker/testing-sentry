import os

import sentry_sdk


sentry_sdk.init(
    dsn=os.environ["SENTRY_DSN"],
    enable_tracing=True,
    debug=True,
)

division_by_zero = 1 / 0
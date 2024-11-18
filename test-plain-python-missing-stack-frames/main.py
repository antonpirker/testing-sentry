import os

import sentry_sdk
from sentry_sdk import capture_exception

sentry_sdk.init(
    dsn=os.environ["SENTRY_DSN"],
    enable_tracing=True,
    debug=True,
    add_full_stack=True,
)


def main():
    foo()


def foo():
    try:
        bar()
    except Exception as e:
        capture_exception(e)


def bar():
    raise Exception("This is a test exception")


if __name__ == "__main__":
    main()


# stack sollte sein?:
# line 25
# line 19
# line 14
# line 29


# but instead is:
# line 25
# line 19
import os
import time

from fastapi import FastAPI, Depends

import sentry_sdk
from sentry_sdk import logger as sentry_logger
from sentry_sdk.crons import monitor
from sentry_sdk.feature_flags import add_feature_flag
from sentry_sdk.consts import VERSION as SENTRY_SDK_VERSION

DIR = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    environment=f"{DIR}-{SENTRY_SDK_VERSION}",
    release=SENTRY_SDK_VERSION,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    debug=True,
    _experiments={
        "enable_logs": True,
    },
    spotlight="http://localhost:9999/api/0/envelope/",
)


app = FastAPI()

def _fibonacci(n):
    print(f"fibonacci {n}")
    time.sleep(0.05)
    if n < 0:
        print("Incorrect input")
    elif n == 0:
        return 0
    elif n == 1 or n == 2:
        return 1
    else:
        return _fibonacci(n-1) + _fibonacci(n-2)


def get_user():
    user = {
      "id": "testuser",
      "username": "Test User",
    }
    sentry_sdk.set_user(user)
    return user


@app.middleware("http")
async def test_middleware(request, call_next):
    print("middleware")
    return await call_next(request)


monitor_config = {
    "schedule": {"type": "crontab", "value": "0 0 * * *"},
    "timezone": "Europe/Vienna",
    # If an expected check-in doesn't come in `checkin_margin`
    # minutes, it'll be considered missed
    "checkin_margin": 10,
    # The check-in is allowed to run for `max_runtime` minutes
    # before it's considered failed
    "max_runtime": 10,
    # It'll take `failure_issue_threshold` consecutive failed
    # check-ins to create an issue
    "failure_issue_threshold": 5,
    # It'll take `recovery_threshold` OK check-ins to resolve
    # an issue
    "recovery_threshold": 5,
}

@app.get("/error")
@monitor(monitor_slug="test-cron", monitor_config=monitor_config)
def error(user=Depends(get_user)):
    # feature flag
    add_feature_flag("test-flag", True)

    # spans
    with sentry_sdk.start_span(name="test-span"):
        with sentry_sdk.start_span(name="test-span-2"):

            # tag
            sentry_sdk.set_tag("test-tag", "test-value")

            # user
            sentry_sdk.set_user(user)

            # breadcrumb
            sentry_sdk.add_breadcrumb(
                category="test-category",
                message="test breadcrumb",
                level="info",
                data={"user": user},
            )

            # context
            sentry_sdk.set_context("test-context", {"text-context-user": user})

            # attachment
            scope = sentry_sdk.get_current_scope()
            scope.add_attachment(bytes=b"Hello World", filename="hello.txt")

            # logs
            sentry_logger.warning("test log")

            # do some work, so we have a profile
            _fibonacci(5)

            # raise an error
            raise ValueError("help! an error!")


@app.get("/")
def index():
    return {
        "hello": "world!",
        "errors-are-here": "http://localhost:5000/error",
    }

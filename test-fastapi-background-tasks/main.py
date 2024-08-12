import os
import time

import sentry_sdk
from sentry_sdk.integrations.starlette import StarletteIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration

from fastapi import FastAPI, BackgroundTasks


sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    environment=os.environ.get("ENV", "test"),
    traces_sample_rate=1.0,
    debug=True,
)


app = FastAPI()


def write_notification(email: str, message=""):
    with sentry_sdk.start_span(op="write_notification", description=f"Notification for {email}"):
        time.sleep(0.1)
        print(f"Notification for {email}: {message}")


@app.get("/")
async def index(background_tasks: BackgroundTasks):
    for x in range(5):
        background_tasks.add_task(write_notification, x, message="some notification")

    return {"message": "Notification sent in the background"}
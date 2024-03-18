from fastapi import FastAPI
from fastapi import Request

import os

import sentry_sdk

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    environment=os.environ.get("ENV", "main2"),
    release="main2@0.0.1",
    # Set rate to 1.0 to capture 100%
    debug=True,
    traces_sample_rate=0,
)


app = FastAPI()

@app.middleware("http")
async def test_middleware(request, call_next):
    print("middleware")
    return await call_next(request)


@app.get("/test2")
def main2_endpoint(request: Request):
    print("main2")
    return {
        "iam": "main2",
        "incoming-headers": dict(request.headers),
    }


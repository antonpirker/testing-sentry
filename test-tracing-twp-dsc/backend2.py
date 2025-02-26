from fastapi import FastAPI
from fastapi import Request

import os

import sentry_sdk


sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN_BACKEND2"),
    environment=os.environ.get("SENTRY_ENVIRONMENT"),
    release="backend2@0.0.1",
    traces_sample_rate=1.0,
    debug=True,
)


app = FastAPI()


@app.middleware("http")
async def test_middleware(request, call_next):
    print("middleware")
    return await call_next(request)


@app.get("/test2")
def backend2_endpoint(request: Request):
    print("backend2")

    return {
        "iam": "backend2",
        "received-headers-from-backend1": dict(request.headers),
    }


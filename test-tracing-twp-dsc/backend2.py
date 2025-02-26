import os

from fastapi import FastAPI, Request

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
    return await call_next(request)


@app.get("/test2")
async def backend2_endpoint(request: Request):
    print("Incoming request (from backend1):")
    print(f"- sentry-trace: {request.headers.get('sentry-trace')}")
    print(f"- baggage: {request.headers.get('baggage')}")

    return {
        "iam": "backend2",
        "received-headers-from-backend1": dict(request.headers),
    }


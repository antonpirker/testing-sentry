import os

import aiohttp

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from utils import format_baggage


# *** SENTRY INITIALIZATION ***

import sentry_sdk
sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN_BACKEND1"),
    environment=os.environ.get("SENTRY_ENVIRONMENT"),
    release="backend1@0.0.1",
    traces_sample_rate=1.0,
    debug=True,
)


app = FastAPI()


# Add CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
    expose_headers=["sentry-trace", "baggage"]  # Expose both sentry-trace and baggage headers
)


@app.middleware("http")
async def test_middleware(request, call_next):
    return await call_next(request)


@app.get("/test1")
async def backend1_endpoint(request: Request):
    print("\nIncoming request (from frontend):")
    print(f"- sentry-trace: {request.headers.get('sentry-trace')}")
    print(f"- baggage: {request.headers.get('baggage')}")
    print(format_baggage(request.headers.get('baggage')))

    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8002/test2') as response:
            print("\nOutgoing request (to backend2):")
            print(f"- sentry-trace: {response.request_info.headers.get('sentry-trace')}")
            print(f"- baggage: {response.request_info.headers.get('baggage')}")
            print(format_baggage(response.request_info.headers.get('baggage')))

            return {
                "iam": "backend1",
                "received": await response.json()
            }

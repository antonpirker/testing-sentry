from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

import requests

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
    print("middleware")
    return await call_next(request)


@app.get("/test1")
def backend1_endpoint():
    print("backend1")
    
    r = requests.get('http://localhost:8002/test2')
    
    return {
        "iam": "backend1",
        "received": r.json()
    }

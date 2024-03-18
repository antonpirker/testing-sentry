from fastapi import FastAPI
import os

import requests

import sentry_sdk

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    environment=os.environ.get("ENV", "main1"),
    release="main1@0.0.1",
    # Set rate to 1.0 to capture 100%
    traces_sample_rate=0.2,
    debug=True,
)


app = FastAPI()

@app.middleware("http")
async def test_middleware(request, call_next):
    print("middleware")
    return await call_next(request)


@app.get("/test1")
def main1_endpoint():
    r = requests.get('http://localhost:5002/test2')
    return {
        "iam": "main1",
        "received": r.json()
    }

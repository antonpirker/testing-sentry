import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import sentry_sdk

from tasks import task_a, task_b

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN", None),
    traces_sample_rate=1.0,
    debug=True,
    # integrations=[
    # ],
)

app = FastAPI()

origins = [
    "http://localhost:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"Hello": "Async World"}


@app.get("/something/{message}")
async def read_something(message: str):
    # task_b.apply_async((message, ), headers={"sentry-propagate-traces": False})
    result = task_b.apply_async((message, ))

    return {"Hello": result.get()}


@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0


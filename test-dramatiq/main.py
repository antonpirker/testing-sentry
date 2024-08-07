import os

import dramatiq

import sentry_sdk
from sentry_sdk.integrations.dramatiq import DramatiqIntegration

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    environment=os.environ.get("ENV", "test"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    debug=True,
    integrations=[
        DramatiqIntegration(),
    ],
    max_request_body_size="always",
)

from dramatiq.brokers.redis import RedisBroker

redis_broker = RedisBroker(host="localhost", port=6379)
dramatiq.set_broker(redis_broker)

@dramatiq.actor(max_retries=0)
def dummy_actor(x, y):
    return x / y


if __name__ == "__main__":
    # dummy_actor(1, 2)
    # dummy_actor.send(3, 4)
    dummy_actor.send(12, 0)

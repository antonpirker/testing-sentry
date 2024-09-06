import asyncio
import os
import redis.asyncio as redis


import sentry_sdk
from sentry_sdk.integrations.redis import RedisIntegration


def init_sentry():  
    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_DSN"),
        enable_tracing=True,
        debug=True,
        send_default_pii=True,
        integrations=[
            RedisIntegration(
                cache_prefixes=["key1", "key3", "key5", "key7", "key9"]
            ), 
        ],
    )


async def main():
    init_sentry()

    r = redis.Redis(host='localhost', port=6379)

    with sentry_sdk.start_transaction(name="testing_async_redis"):
        await r.set("key1", "foo")
        await r.get("key1")
        await r.set("key2", "foo2")
        await r.get("key2")

asyncio.run(main())

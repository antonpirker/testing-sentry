import os
import random 

import redis

import sentry_sdk
from sentry_sdk.integrations.redis import RedisIntegration


LEN = 100
COUNT = 15

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

def main():
    init_sentry()

    with sentry_sdk.start_transaction(name="redis-caching"):
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)

        items = [str(hash(str(x)))*LEN for x in random.sample(range(1, COUNT*5), COUNT)]
        
        for i, item in enumerate(items):
            key = f"key{i}"

            print(f"Getting {key}")
            value = r.get(key)
            if not value:
                print("miss!")
                # here create the cache item (we did this above...)
                print(f"Setting {key}")
                r.set(key+"set", item)
                r.setex(key+"setex", 5, item)
                r.get(key+"get")
                r.mget([key+"mget1", key+"mget2", key+"mget3", ])

                value = item


if __name__ == "__main__":
    main()
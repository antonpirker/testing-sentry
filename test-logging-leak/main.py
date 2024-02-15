import asyncio
import aiohttp

import os
import time

import sentry_sdk

import logging
logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s')

async def main():
    sentry_settings = {
        "dsn": os.getenv("SENTRY_DSN", None),
        "environment": os.getenv("ENV", "local"),
        "traces_sample_rate": 1.0,
        # "send_default_pii": True,
        # "debug": True,
        # "integrations": [],
    }
    print(f"Sentry Settings: {sentry_settings}")

    sentry_sdk.init(**sentry_settings)

    with sentry_sdk.start_transaction(op="function", name="logging-leak"):
        async with aiohttp.ClientSession() as s:
            resp = await s.get(
                "https://example.com/api/v2/session/",
                # "http://auth.docker/api/v2/store/payflow/notify/",
                headers={"Authentication": "SECRET"},
            )
            import ipdb; ipdb.set_trace()
            try:
                resp.raise_for_status()
            except Exception as e:
                import ipdb; ipdb.set_trace()

            time.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
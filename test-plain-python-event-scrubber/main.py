import asyncio
import os

import sentry_sdk
from sentry_sdk.scrubber import EventScrubber


async def main():
    pii_denylist = ["card_details"]
    event_scrubber = EventScrubber(
        send_default_pii=False,
        pii_denylist=pii_denylist,
        recursive=True
    )
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN", None),
        environment=os.getenv("ENV", "local"),
        traces_sample_rate=1.0,
        send_default_pii=False,
        include_local_variables=False,
        event_scrubber=event_scrubber,
        debug=True,
    )

    with sentry_sdk.start_transaction(op="function", name="test-transaction") as trx:
        trx.set_data("card_details", "2222420000001113")  # tags are NOT scrubbed...
        print("Hello, world!")

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import os

import sentry_sdk

def traces_sampler(sampling_context):
    import ipdb; ipdb.set_trace()
    print(f"Traces sampler called with {sampling_context}")
    print(f'Traces sampler transaction name: "{sampling_context["transaction_context"]["name"]}"')

    transaction = sampling_context.get("transaction_context")
    if transaction:
        transaction["tags"] = {
            "testxxx-tag": "testxxx-value",
        }
        
    return 1

async def main():
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN", None),
        environment=os.getenv("ENV", "local"),
        traces_sample_rate=1.0,
        traces_sampler=traces_sampler,
        debug=True,
    )

    with sentry_sdk.start_transaction(op="function", name="transaction-with-traces-sampler-data"):
        print("Hello, world!")

if __name__ == "__main__":
    asyncio.run(main())
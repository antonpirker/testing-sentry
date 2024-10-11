import asyncio
import os

from anthropic import AsyncAnthropic

import sentry_sdk
from sentry_sdk.ai.monitoring import ai_track
from sentry_sdk.integrations.anthropic import AnthropicIntegration


@ai_track("My async AI pipeline")
async def my_pipeline(client):    
    with sentry_sdk.start_transaction(name="anthropic-async"):
        # Async create message
        message = await client.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Hi!",
                }
            ],
            model="claude-3-haiku-20240307",
        )
        print(message.dict())

        # Async create streaming message
        stream = await client.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Hi!",
                }
            ],
            model="claude-3-haiku-20240307",
            stream=True,
        )
        async for event in stream:
            print(event.dict())


async def main():
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN", None),
        environment=os.getenv("ENV", "local"),
        traces_sample_rate=1.0,
        send_default_pii=True,
        debug=True,
        integrations=[
            AnthropicIntegration(include_prompts=True), 
        ],
    )

    client = AsyncAnthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )

    await my_pipeline(client)    


asyncio.run(main())
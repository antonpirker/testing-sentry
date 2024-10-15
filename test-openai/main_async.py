import asyncio
import os

from openai import AsyncOpenAI

import sentry_sdk
from sentry_sdk.ai.monitoring import ai_track
from sentry_sdk.integrations.openai import OpenAIIntegration


@ai_track("My async OpenAI pipeline")
async def my_pipeline(client):    
    with sentry_sdk.start_transaction(name="openai-async"):
        # Sync create message
        message = await client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Hi!",
                }
            ],
            model="gpt-3.5-turbo",
        )
        print("Message:")
        print(message.dict())

        # Async streams are only in beta in OpenAI
        # # Async create streaming message
        # stream = await client.chat.completions.create(
        #     messages=[
        #         {
        #             "role": "user",
        #             "content": "Hi!",
        #         }
        #     ],
        #     model="gpt-3.5-turbo",
        #     stream=True,
        # )
        # print("Message (Stream):")
        # for event in stream:
        #     print(event)


async def main():
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN", None),
        environment=os.getenv("ENV", "local"),
        traces_sample_rate=1.0,
        send_default_pii=True,
        debug=True,
        integrations=[
            OpenAIIntegration(include_prompts=True), 
        ],
    )

    client = AsyncOpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    await my_pipeline(client)    


asyncio.run(main())
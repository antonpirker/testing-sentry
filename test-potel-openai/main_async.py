import asyncio
import os

from openai import AsyncOpenAI

import sentry_sdk
from sentry_sdk.ai.monitoring import ai_track
from sentry_sdk.consts import VERSION as SENTRY_SDK_VERSION
from sentry_sdk.integrations.openai import OpenAIIntegration

DIR = os.path.basename(os.path.dirname(os.path.abspath(__file__)))


@ai_track("My async OpenAI pipeline")
async def my_pipeline(client):
    with sentry_sdk.start_transaction(name="openai-async"):
        # Async create message
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

        # Async embeddings
        result = await client.embeddings.create(
            input="Your text goes here",
            model="text-embedding-3-small",
        )
        embedding = result.data[0].embedding
        print("Embedding:")
        print(len(embedding))

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
        dsn=os.environ.get("SENTRY_DSN"),
        environment=f"{DIR}-{SENTRY_SDK_VERSION}-async",
        release=SENTRY_SDK_VERSION,
        integrations=[
            OpenAIIntegration(include_prompts=True),
        ],
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        debug=True,
        _experiments={
            "enable_logs": True,
        },
        spotlight="http://localhost:9999/api/0/envelope/",
        # Continuous Profiling (comment out profiles_sample_rate if you enable this)
        # profile_session_sample_rate=1.0,
        # profile_lifecycle="trace",
        send_default_pii=True,
    )

    client = AsyncOpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    await my_pipeline(client)


asyncio.run(main())

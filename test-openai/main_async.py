import asyncio
import os

from openai import AsyncOpenAI

import sentry_sdk
from sentry_sdk.ai.monitoring import ai_track
from sentry_sdk.integrations.openai import OpenAIIntegration
from sentry_sdk.integrations.stdlib import StdlibIntegration


@ai_track("My async OpenAI workflow")
async def my_workflow(client):
    with sentry_sdk.start_transaction(name="openai-async"):
        # Responses API
        response = await client.responses.create(
            model="gpt-4o-mini",
            instructions="You are a coding assistant that talks like a pirate.",
            input="How do I check if a Python object is an instance of a class?",
        )
        print("--------------------------------")
        print("Response:")
        print(response.model_dump())

        # Completions API
        message = await client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Hi!",
                }
            ],
            model="gpt-3.5-turbo",
        )
        print("--------------------------------")
        print("Message:")
        print(message.dict())

        # Embeddings API
        embeddings = await client.embeddings.create(
            input="Your text goes here",
            model="text-embedding-3-small",
        )
        embeddings = embeddings.data[0].embedding
        print("--------------------------------")
        print("Embeddings:")
        print(len(embeddings))


async def main():
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN", None),
        environment=os.getenv("ENV", "openai-test-async"),
        traces_sample_rate=1.0,
        send_default_pii=True,
        debug=True,
        integrations=[
            OpenAIIntegration(include_prompts=True),
        ],
        disabled_integrations=[
            StdlibIntegration(),
        ],
    )

    client = AsyncOpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    await my_workflow(client)

    print("--------------------------------")
    print("Done!")


asyncio.run(main())

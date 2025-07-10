import os

from openai import OpenAI

import sentry_sdk
from sentry_sdk.ai.monitoring import ai_track
from sentry_sdk.integrations.openai import OpenAIIntegration


@ai_track("My sync OpenAI pipeline")
def my_pipeline(client):
    with sentry_sdk.start_transaction(name="openai-sync"):
        # Responses API
        response = client.responses.create(
            model="gpt-4o-mini",
            instructions="You are a coding assistant that talks like a pirate.",
            input="How do I check if a Python object is an instance of a class?",
        )
        print("Response:")
        print(response.model_dump())

        # Completions API
        message = client.chat.completions.create(
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

        # Embeddings API
        embeddings = client.embeddings.create(
            input="Your text goes here",
            model="text-embedding-3-small",
        ).data[0].embedding
        print("Embeddings:")
        print(len(embeddings))


def main():
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

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    my_pipeline(client)


if __name__ == "__main__":
    main()

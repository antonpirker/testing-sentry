import os

from openai import OpenAI

import sentry_sdk
from sentry_sdk.ai.monitoring import ai_track
from sentry_sdk.integrations.openai import OpenAIIntegration


@ai_track("My sync OpenAI pipeline")
def my_pipeline(client):
    with sentry_sdk.start_transaction(name="openai-sync"):
        # Sync create message
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

        # Sync embeddings
        embedding = client.embeddings.create(
            input="Your text goes here",
            model="text-embedding-3-small",
        ).data[0].embedding
        print("Embedding:")
        print(len(embedding))

        # Sentry does not instrument streaming OpenAI API calls
        # # Sync create streaming message
        # stream = client.chat.completions.create(
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

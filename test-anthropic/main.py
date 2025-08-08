import os

from anthropic import Anthropic

import sentry_sdk
from sentry_sdk.ai.monitoring import ai_track
from sentry_sdk.integrations.anthropic import AnthropicIntegration


@ai_track("My sync AI pipeline")
def my_pipeline(client):
    with sentry_sdk.start_transaction(name="anthropic-sync"):
        # Sync create message
        message = client.messages.create(
            messages=[
                {
                    "role": "user",
                    "content": "Hi!",
                }
            ],
            model="claude-3-5-haiku-latest",
            max_tokens=1024,
        )
        print("Message:")
        print(message.dict())

        # Sync create streaming message
        stream = client.messages.create(
            messages=[
                {
                    "role": "user",
                    "content": "Hi!",
                }
            ],
            model="claude-3-5-haiku-latest",
            max_tokens=1024,
            stream=True,
        )
        print("Message (Stream):")
        for event in stream:
            print(event.dict())


def main():
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

    client = Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )

    my_pipeline(client)


if __name__ == "__main__":
    main()

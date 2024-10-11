import json
import os

from anthropic import Anthropic

import sentry_sdk
from sentry_sdk.ai.monitoring import ai_track
from sentry_sdk.integrations.anthropic import AnthropicIntegration


def get_weather(location):
    return f"The weather in {location} is sunny with a high of 23°C."


# Define the tool
tools = [
      {
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "The city and state, e.g. San Francisco, CA"
            }
          },
          "required": ["location"]
        }
      }
    ]


@ai_track("My sync tool AI pipeline")
def my_pipeline(client):    
    with sentry_sdk.start_transaction(name="anthropic-sync-tool"):
        # Sync create message using a tool
        message = client.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "What's the weather like in San Francisco, CA?",
                }
            ],
            tools=tools,
            temperature=0,
            model="claude-3-5-sonnet-20240620",
        )
        print("Message:")
        print(message.dict())

        # Sync create streaming message using a tool
        stream = client.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "What's the weather like in San Francisco, CA?",
                }
            ],
            tools=tools,
            temperature=0,
            model="claude-3-5-sonnet-20240620",
            stream=True,
        )

        print("Message (Stream):")
        for event in stream:
            # Int the events is an item with 'type':'tool_use' that should be parsed and then the tool called
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
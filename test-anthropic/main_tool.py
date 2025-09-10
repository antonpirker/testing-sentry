import os

from anthropic import Anthropic

import sentry_sdk
from sentry_sdk.integrations.anthropic import AnthropicIntegration
from sentry_sdk.consts import SPANTEMPLATE


def get_weather(location):
    return f"It is sunny with a high of 23°C."


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


@sentry_sdk.trace(name="Custom AI Agent", template=SPANTEMPLATE.AI_AGENT)
def my_pipeline(client):
    # Sync create message with tools
    message = client.messages.create(
        messages=[
            {
                "role": "user",
                "content": "What's the weather like in San Francisco, CA?",
            }
        ],
        model="claude-3-5-sonnet-20240620",
        tools=tools,
        max_tokens=1024,
        temperature=0,
    )
    print("Message:")
    print(message.dict())
    # If model wants to run a tool, run it.
    if message.stop_reason == "tool_use":
        tool_use_block = message.content[1]
        function_name = tool_use_block.name
        tool_args = tool_use_block.input

        if function_name in globals() and callable(globals()[function_name]):
            tool_result = globals()[function_name](**tool_args)
            print(f"Tool result: {tool_result}")

            # Continue the conversation with the tool result
            response = client.messages.create(
                messages=[
                    {
                        "role": "user",
                        "content": "What's the weather like in San Francisco, CA?",
                    },
                    {
                        "role": "assistant",
                        "content": message.content
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": tool_use_block.id,
                                "content": tool_result
                            }
                        ]
                    }
                ],
                model="claude-3-5-sonnet-20240620",
                tools=tools,
                max_tokens=1024,
                temperature=0,
            )

            print("Final response:")
            print(response.content[0].text)


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

    with sentry_sdk.start_transaction(name="anthropic-sync-tool"):
        my_pipeline(client)


if __name__ == "__main__":
    main()

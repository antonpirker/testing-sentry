import os

import sentry_sdk
from sentry_sdk.integrations.huggingface_hub import HuggingfaceHubIntegration

from huggingface_hub import InferenceClient


TOOLS = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get current temperature for a given location.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "City and country e.g. Paris, France"
                        }
                    },
                    "required": ["location"],
                },
            }
        }
]


def main():
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN", None),
        environment=os.getenv("ENV", "local"),
        traces_sample_rate=1.0,
        send_default_pii=True,
        debug=True,
        integrations=[
            HuggingfaceHubIntegration(include_prompts=True),
        ],
    )

    model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    provider = "featherless-ai"

    client = InferenceClient(
        token=os.getenv("HF_TOKEN", None),
        provider=provider,
    )

    response = client.chat_completion(
        model=model,
        messages=[
        {
            "role": "user",
            "content": "What's the weather like the next 3 days in London, UK?"
        }
        ],
        tools=TOOLS,
        tool_choice="auto",
        frequency_penalty=0.1,
        max_tokens=50,
        presence_penalty=0.2,
        top_p=0.9,
        temperature=0.2,
        stream=False,
    )
    print("--------------------------------")
    print("Output client.chat_completion:")
    print(response)

    # OpenAI compatible API
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Count to 10"},
        ],
        tools=TOOLS,
        tool_choice="auto",
        frequency_penalty=0.1,
        max_tokens=50,
        presence_penalty=0.2,
        top_p=0.9,
        temperature=0.2,
        stream=False,
    )
    print("--------------------------------")
    print("Output client.chat.completions.create:")
    print(response)


if __name__ == "__main__":
    main()

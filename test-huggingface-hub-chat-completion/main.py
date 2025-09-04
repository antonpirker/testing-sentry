import os

import sentry_sdk
from sentry_sdk.integrations.huggingface_hub import HuggingfaceHubIntegration

from huggingface_hub import InferenceClient


TOOLS = [{
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
}]


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

    # model = "meta-llama/Meta-Llama-3-70B-Instruct"
    model = "Qwen/Qwen2.5-72B-Instruct"
    # provider = "hf-inference"

    with sentry_sdk.start_transaction(name="huggingface-hub-chat-completion"):
        client = InferenceClient(
            token=os.getenv("HF_TOKEN", None),
            # provider=provider,
        )

        response = client.chat_completion(
            model=model,
            messages=[
            {
                "role": "user",
                "content": "What is the weather in London, UK?"
            }
            ],
            tools=TOOLS,
            tool_choice="auto",
            frequency_penalty=0.1,
            max_tokens=500,
            presence_penalty=0.2,
            top_p=0.9,
            temperature=0.2,
            stream=True,
        )
        print("--------------------------------")
        print("Output client.chat_completion:")
        for chunk in response:
            print(chunk)

        # OpenAI compatible API
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Should i be nice to my partner today? Short answer yes or no."},
            ],
            tools=TOOLS,
            tool_choice="auto",
            frequency_penalty=0.1,
            max_tokens=50,
            presence_penalty=0.2,
            top_p=0.9,
            temperature=0.2,
            stream=True,
        )
        print("--------------------------------")
        print("Output client.chat.completions.create:")
        for chunk in response:
            print(chunk)


if __name__ == "__main__":
    main()

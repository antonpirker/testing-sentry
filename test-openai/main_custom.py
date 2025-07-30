import os

from openai import OpenAI

import sentry_sdk
from sentry_sdk.integrations.openai import OpenAIIntegration
from sentry_sdk.integrations.stdlib import StdlibIntegration


@sentry_sdk.trace(name="Get Weather", as_type="ai_tool")
def get_weather(lat: float, lng: float) -> str:
    return "sunny"


@sentry_sdk.trace(as_type="ai_chat")
def chat(client, input: str):
    return "Bla"


@sentry_sdk.trace(name="My Agent", as_type="ai_agent")
def my_socalled_agent(client):
    sentry_sdk.update_current_span(attributes={
        "gen_ai.request.model": "gpt-4o-mini",
        "gen_ai.request.available_tools": "[{'type': 'function', 'name': 'get_weather', 'description': 'Get current temperature for provided coordinates in celsius.', 'parameters': {'type': 'object', 'properties': {'latitude': {'type': 'number'}, 'longitude': {'type': 'number'}}, 'required': ['latitude', 'longitude'], 'additionalProperties': False}, 'strict': True}]",
        "gen_ai.request.messages": "What is the weather in Paris?",
        "gen_ai.request.temperature": 0.2,
        "gen_ai.request.top_k": 0.7,
        "gen_ai.": "",
    })

    chat(client, "What is the weather in Paris?")
    get_weather(48.8566, 2.3522)
    chat(client, "What is the weather in Paris2?")

    sentry_sdk.update_current_span(attributes={
        "gen_ai.response.model": "gpt-4o-mini-xxx",
        "gen_ai.response.text": "Nice and sunny",
        "gen_ai.usage.input_tokens": 10,
        "gen_ai.usage.output_tokens": 10,
        "gen_ai.usage.total_tokens": 20,
    })


def main():
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN", None),
        environment=os.getenv("ENV", "openai-test-sync"),
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        send_default_pii=True,
        debug=True,
        integrations=[
            OpenAIIntegration(include_prompts=True),
        ],
        disabled_integrations=[
            StdlibIntegration(),
        ],
    )

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    with sentry_sdk.start_transaction(name="main"):
        my_socalled_agent(client)

    print("--------------------------------")
    print("Done!")


if __name__ == "__main__":
    main()

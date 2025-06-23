import asyncio
import os
import random
import time

from pydantic import BaseModel

import sentry_sdk
from sentry_sdk.integrations.openai_agents import OpenAIAgentsIntegration

import agents


@agents.function_tool
def random_number(max: int) -> int:
    """
    Generate a random number up to the provided maximum.
    """
    # 1/0
    time.sleep(0.34)
    return random.randint(0, max)


@agents.function_tool
def multiply(x: int, y: int) -> int:
    """Simple multiplication by two."""
    time.sleep(0.56)
    # 1/0
    return x * y


@agents.function_tool
def magic_tool() -> int:
    """A magic tool that always returns 123"""
    return 123


@agents.function_tool
def query_database(query: str) -> str:
    """A tool to query a database"""
    return "hello"


class FinalResult(BaseModel):
    number: int


multiply_agent = agents.Agent(
    name="Multiply Agent",
    instructions="Multiply the number x by the number y and then return the final result.",
    tools=[multiply],
    model="gpt-4.1-mini",
    output_type=FinalResult,
)


random_number_agent = agents.Agent(
    name="Random Number Agent",
    instructions="Generate a random number. If it's even, hand off to multiply agent to multiply by 2. If it's odd, hand off to the multiply agent to multiply by 30.",
    tools=[random_number, magic_tool, query_database],
    output_type=FinalResult,
    handoffs=[multiply_agent],
    model="gpt-4o-mini",
    model_settings=agents.ModelSettings(
        temperature=0.1,
        top_p=0.2,
        frequency_penalty=0.3,
        presence_penalty=0.4,
        max_tokens=100,
    )
)


from sentry_sdk.integrations.stdlib import StdlibIntegration
async def main() -> None:
    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_DSN"),
        environment=os.environ.get("ENV", "test"),
        traces_sample_rate=1.0,
        send_default_pii=True,
        integrations=[OpenAIAgentsIntegration()],
        disabled_integrations=[
            StdlibIntegration(),
        ],
        debug=True,
    )

    user    = {"id": "22", "email": "user22@test.com"}
    sentry_sdk.set_user(user)
    sentry_sdk.set_tag("my_custom_tag", "value_one")

    await agents.Runner.run(
        random_number_agent,
        input=f"Generate a random number between 0 and {10}.",
    )

    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())

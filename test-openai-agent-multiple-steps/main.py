import asyncio
import os
import random

from agents import Agent, Runner, function_tool, ModelSettings
from pydantic import BaseModel


import sentry_sdk
from sentry_sdk.integrations.openai_agents import OpenAIAgentsIntegration
from sentry_sdk.integrations.stdlib import StdlibIntegration


@function_tool()
def random_number(max: int) -> int:
    """Generate a random number between 0 and the provided maximum value.

    This tool generates a random integer within the specified range, inclusive of 0
    and exclusive of the maximum value.

    Args:
        max: The upper bound for the random number (exclusive). Must be positive.

    Returns:
        A random integer between 0 and max-1 (inclusive).

    Example:
        random_number(10) might return 7
    """

    return random.randint(0, max)


@function_tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together and return the result.

    This tool adds two integers together and returns the result.

    Args:
        a: The first number to add
        b: The second number to add

    Returns:
        The sum of a and b

    Example:
        add_numbers(1, 2) might return 3
    """

    return a + b


class FinalResult(BaseModel):
    number: float


INSTRUCTIONS = (
    "You are a helpful assistant and can use tools to help the user."
)


math_agent = Agent(
    name="MathAgent",
    instructions=INSTRUCTIONS,
    tools=[random_number, add_numbers],
    model="gpt-4o",
    output_type=FinalResult,
    model_settings=ModelSettings(
        temperature=0.1,
        top_p=0.2,
        frequency_penalty=0.3,
        presence_penalty=0.4,
        max_tokens=500,
        # include_usage=True,
    ),
)


PROMPT = (
    "Give me three random numbers. The between 0 and 10, the second between 0 and 100 and the third between 0 and 1000. Then add them together."
)


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

    await Runner.run(math_agent, input=PROMPT)

    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())

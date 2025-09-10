import asyncio
import os

from agents import Agent, Runner, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel
from simpleeval import simple_eval

import sentry_sdk
from sentry_sdk.integrations.openai_agents import OpenAIAgentsIntegration
from sentry_sdk.integrations.openai import OpenAIIntegration
from sentry_sdk.integrations.stdlib import StdlibIntegration


@function_tool
def calculate(expression: str):
    """
    A tool for evaluating mathematical expressions.
    Example expressions:
        '1.2 * (2 + 4.5)', '12.7 cm to inch'
        'sin(45 deg) ^ 2'
    """
    # Remove any whitespace
    expression = expression.strip()

    # Evaluate the expression
    result = simple_eval(expression)

    # If the result is a float, round it to 6 decimal places
    if isinstance(result, float):
        result = round(result, 6)

    return result


INSTRUCTIONS = (
    "You are solving math problems. "
    "Use the calculator when necessary. "
    "When you give the final answer, "
    "provide an explanation for how you arrived at it. "
)

claude_client = AsyncOpenAI(base_url="https://api.anthropic.com/v1/", api_key=os.environ.get("ANTHROPIC_API_KEY"))

math_agent = Agent(
    name="MathAgent",
    instructions=INSTRUCTIONS,
    tools=[calculate],
    model=OpenAIChatCompletionsModel(
        model="claude-3-7-sonnet-20250219",
        openai_client=claude_client,
    ),
    # model="gpt-4o",
)


PROMPT = (
    "What is 12 * 13? use the calculate tool."
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
            OpenAIIntegration(),
        ],
        debug=True,
    )

    result = await Runner.run(math_agent, input=PROMPT)
    print(result)

    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())

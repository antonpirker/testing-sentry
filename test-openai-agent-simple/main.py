import asyncio
import os

from agents import Agent, Runner, function_tool
from pydantic import BaseModel
from simpleeval import simple_eval

import sentry_sdk
from sentry_sdk.integrations.openai_agents import OpenAIAgentsIntegration
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


class FinalResult(BaseModel):
    number: float


INSTRUCTIONS = (
    "You are solving math problems. "
    "Reason step by step. "
    "Use the calculator when necessary. "
    "When you give the final answer, "
    "provide an explanation for how you arrived at it. "
)


math_agent = Agent(
    name="MathAgent",
    instructions=INSTRUCTIONS,
    tools=[calculate],
    model="gpt-4o",
    output_type=FinalResult,
)


PROMPT = (
    "A taxi driver earns $9461 per 1-hour of work. "
    "If he works 12 hours a day and in 1 hour "
    "he uses 12 liters of petrol with a price of $134 for 1 liter. "
    "How much money does he earn in one day?"
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
    #     debug=True,
    )

    await Runner.run(math_agent, input=PROMPT)

    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())

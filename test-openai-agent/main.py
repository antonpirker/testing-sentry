import asyncio
import os
import random
import time

from pydantic import BaseModel

import sentry_sdk
from sentry_sdk.integrations.openai_agents import OpenAIAgentsIntegration

from agents import Agent, Runner, function_tool, ModelSettings


@function_tool
def random_number(max: int) -> int:
    """
    Generate a random number up to the provided maximum.
    """
    time.sleep(0.34)
    return random.randint(0, max)


@function_tool
def multiply(x: int, y: int) -> int:
    """Simple multiplication by two."""
    time.sleep(0.56)
    return x * y


@function_tool
def magic_tool() -> int:
    """A magic tool that always returns 123"""
    return 123


@function_tool
def query_database(query: str) -> str:
    """A tool to query a database"""
    return "hello"


class FinalResult(BaseModel):
    number: int


multiply_agent = Agent(
    name="Multiply Agent",
    instructions="Multiply the number x by the number y and then return the final result.",
    tools=[multiply],
    model="gpt-4.1-mini",
    output_type=FinalResult,
)

random_number_agent = Agent(
    name="Random Number Agent",
    instructions="Generate a random number. If it's even, hand off to multiply agent to multiply by 2. If it's odd, hand off to the multiply agent to multiply by 30.",
    tools=[random_number, magic_tool, query_database],
    output_type=FinalResult,
    handoffs=[multiply_agent],
    model="gpt-4o-mini",
    model_settings=ModelSettings(
        temperature=0.1,
        top_p=0.2,
        frequency_penalty=0.3,
        presence_penalty=0.4,
        max_tokens=100,
    )
)



PROMPT = (
    "You are a helpful research assistant. Given a query, come up with a set of web searches "
    "to perform to best answer the query. Output between 5 and 20 terms to query for."
)


class WebSearchItem(BaseModel):
    reason: str
    "Your reasoning for why this search is important to the query."

    query: str
    "The search term to use for the web search."


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem]
    """A list of web searches to perform to best answer the query."""


planner_agent = Agent(
    name="PlannerAgent",
    instructions=PROMPT,
    model="gpt-4.1-nano",
    output_type=WebSearchPlan,
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
    #     debug=True,
    )

    # await Runner.run(
    #     planner_agent,
    #     input="Whats the best snowboard?",
    # )
    user    = {"id": "22", "email": "user22@test.com"}
    sentry_sdk.set_user(user)
    sentry_sdk.set_tag("my_custom_tag", "value_one")

    await Runner.run(
        random_number_agent,
        input=f"Generate a random number between 0 and {10}.",
    )

    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())

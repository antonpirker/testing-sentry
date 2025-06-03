import asyncio
import os
import random
import time
from typing import Any

from pydantic import BaseModel

import sentry_sdk
from sentry_sdk.integrations.openai_agents import SentryRunHooks
from sentry_sdk.integrations.openai_agents import OpenAIAgentsIntegration

import agents
from agents import Agent, Runner, function_tool


# class CustomAgentHooks(AgentHooks):
#     def __init__(self, display_name: str):
#         self.event_counter = 0
#         self.display_name = display_name
#         self.current_transaction = None
#         self.current_span = None

#     async def on_start(self, context: RunContextWrapper, agent: Agent) -> None:
#         import ipdb; ipdb.set_trace()
#         self.event_counter += 1
#         print(f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} started")

#     async def on_end(self, context: RunContextWrapper, agent: Agent, output: Any) -> None:
#         import ipdb; ipdb.set_trace()
#         self.event_counter += 1
#         print(
#             f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} ended with output {output}"
#         )

#     async def on_handoff(self, context: RunContextWrapper, agent: Agent, source: Agent) -> None:
#         import ipdb; ipdb.set_trace()
#         self.event_counter += 1
#         print(
#             f"### ({self.display_name}) {self.event_counter}: Agent {source.name} handed off to {agent.name}"
#         )

#     async def on_tool_start(self, context: RunContextWrapper, agent: Agent, tool: Tool) -> None:
#         import ipdb; ipdb.set_trace()
#         self.event_counter += 1
#         print(
#             f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} started tool {tool.name}"
#         )

#     async def on_tool_end(
#         self, context: RunContextWrapper, agent: Agent, tool: Tool, result: str
#     ) -> None:
#         import ipdb; ipdb.set_trace()
#         self.event_counter += 1
#         print(
#             f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} ended tool {tool.name} with result {result}"
#         )


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


class FinalResult(BaseModel):
    number: int


multiply_agent = Agent(
    name="Multiply Agent",
    instructions="Multiply the number x by the number y and then return the final result.",
    tools=[multiply],
    output_type=FinalResult,
    # hooks=CustomAgentHooks(display_name="Multiply Agent"),
)

start_agent = Agent(
    name="Start Agent",
    instructions="Generate a random number. If it's even, hand off to multiply agent to multiply by 2. If it's odd, hand off to the multiply agent to multiply by 3.",
    tools=[random_number],
    output_type=FinalResult,
    handoffs=[multiply_agent],
    # hooks=CustomAgentHooks(display_name="Start Agent"),
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
    model="gpt-4o",
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

    with sentry_sdk.start_transaction(name="main"):
        # await Runner.run(
        #     planner_agent,
        #     input="Whats the best snowboard?",
        # )
        await Runner.run(
            start_agent,
            input=f"Generate a random number between 0 and {10}.",
            hooks=SentryRunHooks(),
        )

    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())

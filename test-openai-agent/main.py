import asyncio
import os

import agents

from my_agents import reasoning_agent
from my_agents import random_number_agent, random_number_agent_claude
# from my_agents import multiply_agent, multiply_agent_claude

import sentry_sdk
from sentry_sdk.integrations.openai_agents import OpenAIAgentsIntegration
from sentry_sdk.integrations.stdlib import StdlibIntegration

async def run_agents_using_openai():
    print("\n[OPENAI] Running first request (will create cache)...")
    result1 = await agents.Runner.run(
        random_number_agent,
        input=f"Generate a random number between 0 and {10}.",
    )

    print("[OPENAI] First request usage:")
    for response in result1.raw_responses:
        print(response.usage)

    print("\n[OPENAI] Waiting 2 seconds before second request...")
    await asyncio.sleep(2)

    print("[OPENAI] Running second request (should use cached tokens)...")
    result2 = await agents.Runner.run(
        random_number_agent,
        input=f"Generate a random number between 0 and {15}.",
    )

    print("[OPENAI] Second request usage:")
    for response in result2.raw_responses:
        print(response.usage)

    ## Run reasoning agent
    print("[OPENAI] Running reasoning agent")
    result3 = await agents.Runner.run(
        reasoning_agent,
        input=f"Solve this step by step: If I have 15 apples and I give away 1/3 of them, then buy 8 more, how many apples do I have? Show your reasoning.",
    )

    print("[OPENAI] Reasoning agent usage:")
    for response in result3.raw_responses:
        print(response.usage)


async def run_agents_using_claude():
    print("\n[CLAUDE] Running first request (will create cache)...")
    result1 = await agents.Runner.run(
        random_number_agent_claude,
        input=f"Generate a random number between 0 and {10}.",
    )

    print("[CLAUDE] First request usage:")
    for response in result1.raw_responses:
        print(response.usage)

    print("\n[CLAUDE] Waiting 2 seconds before second request...")
    await asyncio.sleep(2)

    print("[CLAUDE] Running second request (should use cached tokens)...")
    result2 = await agents.Runner.run(
        random_number_agent_claude,
        input=f"Generate a random number between 0 and {15}.",
    )

    print("[CLAUDE] Second request usage:")
    for response in result2.raw_responses:
        print(response.usage)


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

    user = {"id": "22", "email": "user22@test.com"}
    sentry_sdk.set_user(user)
    sentry_sdk.set_tag("my_custom_tag", "value_one")

    with sentry_sdk.start_transaction(name="root-transaction"):
        await run_agents_using_openai()
        await run_agents_using_claude()

    print("\nDone!")


if __name__ == "__main__":
    asyncio.run(main())

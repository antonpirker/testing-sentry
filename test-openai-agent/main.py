import asyncio
import os

import agents

# from my_agents import reasoning_agent
from my_agents import random_number_agent
# from my_agents import multiply_agent

import sentry_sdk
from sentry_sdk.integrations.openai_agents import OpenAIAgentsIntegration
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
        debug=False,
    )

    user = {"id": "22", "email": "user22@test.com"}
    sentry_sdk.set_user(user)
    sentry_sdk.set_tag("my_custom_tag", "value_one")

    # Run multiple requests to see caching in action
    print("\nRunning first request (will create cache)...")
    result1 = await agents.Runner.run(
        random_number_agent,
        input=f"Generate a random number between 0 and {10}.",
    )

    print("First request usage:")
    for response in result1.raw_responses:
        print(response.usage)

    # Wait a moment but not too long (cache expires after ~5-10 minutes)
    print("\nWaiting 2 seconds before second request...")
    await asyncio.sleep(2)

    # Run agent the second time to see if it uses cached tokens
    print("Running second request (should use cached tokens)...")
    result2 = await agents.Runner.run(
        random_number_agent,
        input=f"Generate a random number between 0 and {15}.",
    )

    print("Second request usage:")
    for response in result2.raw_responses:
        print(response.usage)

    ## Run reasoning agent
    # print("Running reasoning agent")
    # result3 = await agents.Runner.run(
    #     reasoning_agent,
    #     input=f"Solve this step by step: If I have 15 apples and I give away 1/3 of them, then buy 8 more, how many apples do I have? Show your reasoning.",
    # )

    # print("Reasoning agent usage:")
    # for response in result3.raw_responses:
    #     print(response.usage)

    print("\nDone!")


if __name__ == "__main__":
    asyncio.run(main())

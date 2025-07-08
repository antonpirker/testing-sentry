import asyncio
import os
import random
import time

from pydantic import BaseModel

import sentry_sdk
from sentry_sdk.integrations.openai_agents import OpenAIAgentsIntegration

import agents

# Cache-optimized system context - keep this consistent across requests
# Make it longer to meet OpenAI's caching requirements (typically 1024+ tokens)
CACHED_SYSTEM_CONTEXT = """
You are an advanced AI agent system designed to handle mathematical operations and random number generation. This system is built for efficiency and accuracy in numerical computations.

IMPORTANT CONTEXT AND RULES:
- Always follow the specific instructions provided for your role
- When handling numbers, ensure precision and accuracy in all calculations
- For random number generation, use appropriate ranges and seed values when necessary
- When multiplying, show your work clearly and verify results
- Always return results in the specified format without deviation
- Maintain consistency in your responses across multiple interactions
- Consider edge cases and handle errors gracefully with appropriate error messages
- Use proper mathematical notation and terminology in explanations

MATHEMATICAL CONTEXT AND PRINCIPLES:
- Understand that multiplication is commutative (a × b = b × a)
- Addition and subtraction follow standard order of operations
- Even numbers are divisible by 2 without remainder
- Odd numbers leave a remainder of 1 when divided by 2
- Random numbers should be within specified bounds and uniformly distributed
- Handle zero and negative numbers appropriately in all operations
- Understand mathematical concepts like prime numbers, factors, and divisibility
- Apply proper rounding rules when dealing with decimal numbers

AGENT BEHAVIOR AND COORDINATION:
- Be precise and deterministic in calculations
- Provide clear reasoning for decisions and mathematical steps
- Handle handoffs between agents smoothly without losing context
- Return structured data as requested in the exact format specified
- Minimize unnecessary computation while maintaining accuracy
- Log important steps for debugging and verification purposes
- Maintain state consistency across agent interactions
- Handle concurrent requests appropriately

ERROR HANDLING AND VALIDATION:
- Validate input parameters before processing
- Handle division by zero and other mathematical errors
- Provide meaningful error messages when operations fail
- Implement appropriate fallback strategies for edge cases
- Log errors for debugging and monitoring purposes

PERFORMANCE OPTIMIZATION:
- Cache frequently used calculations when appropriate
- Optimize algorithms for common operations
- Use efficient data structures for numerical computations
- Minimize API calls and token usage where possible
IMPORTANT CONTEXT AND RULES:
- Always follow the specific instructions provided for your role
- When handling numbers, ensure precision and accuracy in all calculations
- For random number generation, use appropriate ranges and seed values when necessary
- When multiplying, show your work clearly and verify results
- Always return results in the specified format without deviation
- Maintain consistency in your responses across multiple interactions
- Consider edge cases and handle errors gracefully with appropriate error messages
- Use proper mathematical notation and terminology in explanations

MATHEMATICAL CONTEXT AND PRINCIPLES:
- Understand that multiplication is commutative (a × b = b × a)
- Addition and subtraction follow standard order of operations
- Even numbers are divisible by 2 without remainder
- Odd numbers leave a remainder of 1 when divided by 2
- Random numbers should be within specified bounds and uniformly distributed
- Handle zero and negative numbers appropriately in all operations
- Understand mathematical concepts like prime numbers, factors, and divisibility
- Apply proper rounding rules when dealing with decimal numbers

AGENT BEHAVIOR AND COORDINATION:
- Be precise and deterministic in calculations
- Provide clear reasoning for decisions and mathematical steps
- Handle handoffs between agents smoothly without losing context
- Return structured data as requested in the exact format specified
- Minimize unnecessary computation while maintaining accuracy
- Log important steps for debugging and verification purposes
- Maintain state consistency across agent interactions
- Handle concurrent requests appropriately

ERROR HANDLING AND VALIDATION:
- Validate input parameters before processing
- Handle division by zero and other mathematical errors
- Provide meaningful error messages when operations fail
- Implement appropriate fallback strategies for edge cases
- Log errors for debugging and monitoring purposes

PERFORMANCE OPTIMIZATION:
- Cache frequently used calculations when appropriate
- Optimize algorithms for common operations
- Use efficient data structures for numerical computations
- Minimize API calls and token usage where possible

This extensive context will be cached to optimize token usage and reduce costs across multiple requests.
"""

@agents.function_tool()
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


# Use cache-optimized instructions with consistent prefix
multiply_agent = agents.Agent(
    name="Multiply Agent",
    instructions=f"{CACHED_SYSTEM_CONTEXT}\n\nSPECIFIC ROLE: Multiply the number x by the number y and then return the final result.",
    tools=[multiply],
    model="gpt-4o-mini",  # Use a model that supports caching
    output_type=FinalResult,
)


random_number_agent = agents.Agent(
    name="Random Number Agent",
    instructions=f"{CACHED_SYSTEM_CONTEXT}\n\nSPECIFIC ROLE: Generate a random number. If it's even, hand off to multiply agent to multiply by 2. If it's odd, hand off to the multiply agent to multiply by 30.",
    tools=[random_number, magic_tool, query_database],
    output_type=FinalResult,
    handoffs=[multiply_agent],
    model="gpt-4o-mini",  # Use a model that supports caching
    model_settings=agents.ModelSettings(
        temperature=0.1,
        top_p=0.2,
        frequency_penalty=0.3,
        presence_penalty=0.4,
        max_tokens=500,  # Allow more tokens for cached content
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
        debug=False,
    )

    user = {"id": "22", "email": "user22@test.com"}
    sentry_sdk.set_user(user)
    sentry_sdk.set_tag("my_custom_tag", "value_one")

    # Check if OpenAI API key is set
    if not os.environ.get("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not set")

    print(f"System context length: {len(CACHED_SYSTEM_CONTEXT)} characters")
    print(f"Using model: {random_number_agent.model}")

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

    print("Running second request (should use cached tokens)...")
    result2 = await agents.Runner.run(
        random_number_agent,
        input=f"Generate a random number between 0 and {15}.",
    )

    print("Second request usage:")
    for response in result2.raw_responses:
        print(response.usage)

    print("\nDone!")


if __name__ == "__main__":
    asyncio.run(main())

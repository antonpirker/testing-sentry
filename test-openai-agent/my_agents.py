import agents
import os

from pydantic import BaseModel
from my_tools import multiply, random_number, magic_tool, query_database


openai_client = agents.AsyncOpenAI(api_key=os.environ.get("MY_OPENAI_API_KEY"))
claude_client = agents.AsyncOpenAI(api_key=os.environ.get("MY_ANTHROPIC_API_KEY"), base_url="https://api.anthropic.com/v1/")


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

class FinalResult(BaseModel):
    number: int


multiply_agent = agents.Agent(
    name="Multiply Agent",
    instructions=f"{CACHED_SYSTEM_CONTEXT}\n\nSPECIFIC ROLE: Multiply the number x by the number y and then return the final result.",
    tools=[multiply],
    model=agents.OpenAIResponsesModel(
        model="gpt-4o-mini",
        openai_client=openai_client,
    ),
    output_type=FinalResult,
)


random_number_agent = agents.Agent(
    name="Random Number Agent",
    instructions=f"{CACHED_SYSTEM_CONTEXT}\n\nSPECIFIC ROLE: Generate a random number. If it's even, hand off to multiply agent to multiply by 2. If it's odd, hand off to the multiply agent to multiply by 30.",
    tools=[random_number, magic_tool, query_database],
    handoffs=[multiply_agent],
    model=agents.OpenAIResponsesModel(
        model="gpt-4o-mini",
        openai_client=openai_client,
    ),
    model_settings=agents.ModelSettings(
        temperature=0.1,
        top_p=0.2,
        frequency_penalty=0.3,
        presence_penalty=0.4,
        max_tokens=500,
    ),
    output_type=FinalResult,
)


reasoning_agent = agents.Agent(
    name="Reasoning Agent",
    output_type=str,  # Use simple string output instead of structured
    model=agents.OpenAIChatCompletionsModel(
        model="o1-mini",
        openai_client=openai_client,
    ),
)


multiply_agent_claude = agents.Agent(
    name="Multiply Agent",
    instructions=f"{CACHED_SYSTEM_CONTEXT}\n\nSPECIFIC ROLE: Multiply the number x by the number y and then return the final result.",
    tools=[multiply],
    model=agents.OpenAIChatCompletionsModel(
        model="claude-3-7-sonnet-20250219",
        openai_client=claude_client,
    ),
    # no structured output for other models (output_type not supported)
)

random_number_agent_claude = agents.Agent(
    name="Random Number Agent",
    instructions=f"{CACHED_SYSTEM_CONTEXT}\n\nSPECIFIC ROLE: Generate a random number. If it's even, hand off to multiply agent to multiply by 2. If it's odd, hand off to the multiply agent to multiply by 30.",
    tools=[random_number, magic_tool, query_database],
    handoffs=[multiply_agent_claude],
    model=agents.OpenAIChatCompletionsModel(
        model="claude-3-7-sonnet-20250219",
        openai_client=claude_client,
    ),
    model_settings=agents.ModelSettings(
        temperature=0.1,
        max_tokens=500,
        # other settings not supported for Claude models
    )
    # no structured output for other models (output_type not supported)
)

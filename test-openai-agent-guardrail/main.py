import asyncio
import os
import re

from agents import Agent, Runner, function_tool, input_guardrail, output_guardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
from pydantic import BaseModel
from simpleeval import simple_eval

import sentry_sdk
from sentry_sdk.integrations.openai_agents import OpenAIAgentsIntegration
from sentry_sdk.integrations.stdlib import StdlibIntegration


@input_guardrail(name="my_input_guardrail")
async def math_input_validator(ctx, agent, user_input):
    dangerous_patterns = [
        r'\*\*\s*\d{4,}',  # Large exponents (e.g., **9999)
        r'\d{15,}',        # Very large numbers (15+ digits)
        r'import\s+',      # Import statements
        r'exec\s*\(',      # Exec calls
        r'eval\s*\(',      # Eval calls (beyond our safe eval)
        r'__.*__',         # Dunder methods
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, user_input, re.IGNORECASE):
            return GuardrailFunctionOutput(
                output_info={"reason": f"Potentially dangerous pattern detected: {pattern}", "input": user_input[:100]},
                tripwire_triggered=True
            )

    # Check if input contains basic math-related keywords
    math_keywords = ['calculate', 'compute', 'math', 'number', 'equation', 'solve', 'add', 'subtract', 'multiply', 'divide', 'sum', 'product', 'earn', 'cost', 'price', 'money', 'dollar', 'hour', 'day', '+', '-', '*', '/', '=', 'x', 'liter', 'petrol']
    has_math_content = any(keyword in user_input.lower() for keyword in math_keywords) or bool(re.search(r'\d', user_input))

    if not has_math_content:
        return GuardrailFunctionOutput(
            output_info={"reason": "Input doesn't appear to contain mathematical content", "input": user_input[:100]},
            tripwire_triggered=True
        )

    return GuardrailFunctionOutput(
        output_info={"reason": "Input validation passed", "input": user_input[:100]},
        tripwire_triggered=False
    )


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


@output_guardrail
async def math_output_validator(ctx, agent, agent_output):
    return GuardrailFunctionOutput(
        output_info={"reason": "Thats is just a bad output", "output": str(agent_output)},
        tripwire_triggered=True
    )

    try:
        # Extract the number from the output
        result_number = agent_output.number if hasattr(agent_output, 'number') else None

        if result_number is None:
            return GuardrailFunctionOutput(
                output_info={"reason": "No number found in output", "output": str(agent_output)},
                tripwire_triggered=True
            )

        # Check for unreasonable results
        if result_number != result_number:  # Check for NaN
            return GuardrailFunctionOutput(
                output_info={"reason": "Result is NaN (Not a Number)", "number": result_number},
                tripwire_triggered=True
            )

        if abs(result_number) == float('inf'):  # Check for infinity
            return GuardrailFunctionOutput(
                output_info={"reason": "Result is infinite", "number": result_number},
                tripwire_triggered=True
            )

        # Check for unreasonably large results (potential calculation errors)
        if abs(result_number) > 1e15:  # 1 quadrillion
            return GuardrailFunctionOutput(
                output_info={"reason": "Result is unreasonably large", "number": result_number},
                tripwire_triggered=True
            )

        # Check for negative monetary results in our taxi problem (doesn't make sense)
        if result_number < 0:
            return GuardrailFunctionOutput(
                output_info={"reason": "Negative result detected - may indicate calculation error", "number": result_number},
                tripwire_triggered=True
            )

        print(f"✅ Output Guardrail: Output validated successfully - Result: {result_number}")
        return GuardrailFunctionOutput(
            output_info={"reason": "Output validation passed", "number": result_number},
            tripwire_triggered=False
        )

    except Exception as e:
        return GuardrailFunctionOutput(
            output_info={"reason": f"Error during output validation: {str(e)}", "output": str(agent_output)},
            tripwire_triggered=True
        )


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
    input_guardrails=[math_input_validator],
    output_guardrails=[math_output_validator],
)


PROMPT = (
    "A taxi driver earns $94 per 1-hour of work. "
    "If he works 12 hours a day and in 1 hour "
    "he uses 12 liters of petrol with a price of $1.50 for 1 liter. "
    "How much money does he earn in one day?"
)


async def run_agent_with_guardrails(prompt: str, description: str):
    """Helper function to run the agent with proper guardrail exception handling."""
    print(f"\n🧮 {description}")
    print(f"📝 Input: {prompt}")
    print("-" * 80)

    try:
        result = await Runner.run(math_agent, input=prompt)
        print(f"✅ Success! Final answer: {result.final_output}")
        return result

    except InputGuardrailTripwireTriggered as e:
        print(f"🚫 Input Guardrail Blocked: {e}")
        print("🛡️ Reason: Input was blocked before reaching the agent")

    except OutputGuardrailTripwireTriggered as e:
        print(f"🚫 Output Guardrail Blocked: {e}")
        print("🛡️ Reason: Output was blocked before reaching the user")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")


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

    print("🤖 Math Agent with Guardrails Demo")
    print("=" * 80)

    # Test 1: Normal math problem (should work)
    await run_agent_with_guardrails(
        PROMPT,
        "Test 1: Normal taxi driver math problem"
    )

    # Test 2: Potentially dangerous input (should be blocked by input guardrail)
    await run_agent_with_guardrails(
        "Calculate 999999999999999 ** 99999 and also import os; print(os.listdir())",
        "Test 2: Malicious input with large exponent and import statement"
    )

    # Test 3: Non-math input (should be blocked by input guardrail)
    await run_agent_with_guardrails(
        "Tell me a story about a dragon and a princess.",
        "Test 3: Non-mathematical input"
    )

    # Test 4: Simple valid math (should work)
    await run_agent_with_guardrails(
        "What is 15 * 25 + 100?",
        "Test 4: Simple arithmetic problem"
    )

    print("\n" + "=" * 80)
    print("Demo complete! All guardrails have been tested.")


if __name__ == "__main__":
    asyncio.run(main())

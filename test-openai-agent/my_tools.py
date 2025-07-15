import time
import random

import agents


@agents.function_tool()
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
    # 1/0
    time.sleep(0.34)
    return random.randint(0, max)


@agents.function_tool
def multiply(x: int, y: int) -> int:
    """Multiply two numbers together and return the result.

    This tool performs mathematical multiplication of two integer values.

    Args:
        x: The first number to multiply
        y: The second number to multiply

    Returns:
        The product of x multiplied by y

    Example:
        multiply(6, 7) returns 42
    """
    time.sleep(0.56)
    # 1/0
    return x * y


@agents.function_tool
def magic_tool() -> int:
    """A utility tool that always returns the magic number 123.

    This tool provides a constant value and can be used for testing
    or as a placeholder in calculations.

    Returns:
        Always returns the integer 123

    Example:
        magic_tool() always returns 123
    """
    return 123


@agents.function_tool
def query_database(query: str) -> str:
    """Execute a database query and return results.

    This tool simulates a database query operation. Currently returns
    a placeholder response for testing purposes.

    Args:
        query: The database query string to execute

    Returns:
        Query results as a string (currently returns "hello" for testing)

    Example:
        query_database("SELECT * FROM users") returns "hello"
    """
    return "hello"

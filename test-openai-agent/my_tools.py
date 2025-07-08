import time
import random

import agents


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

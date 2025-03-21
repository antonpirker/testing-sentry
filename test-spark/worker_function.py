# worker_function.py

def successful_task(x):
    """A task that will succeed."""
    return f"Successfully processed {x}"

def failing_task(x):
    """A task that will raise an exception to test error reporting."""
    if x % 149 == 0:
        # This will fail for every multiple of 5
        raise ValueError(f"Error processing value {x}")
    return f"Processed {x}"
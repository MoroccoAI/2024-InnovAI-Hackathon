import functools
import time
from typing import Callable, Any, Tuple


def measure_latency(func: Callable) -> Callable:
    """
    A decorator that measures the execution time of a function.
    Returns both the function result and its execution time.
    
    Args:
        func: The function to measure execution time for
        
    Returns:
        A wrapped function that returns (result, execution_time)
    """
    @functools.wraps(func) 
    def wrapper(*args, **kwargs) -> Tuple[Any, float]:
        # Record start time
        start_time = time.perf_counter()
        
        # Execute function
        result = func(*args, **kwargs)
        
        # Calculate elapsed time
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        
        # Return both the function result and the execution time
        return result, execution_time
        
    return wrapper


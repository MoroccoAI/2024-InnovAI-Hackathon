import functools
import tracemalloc
from typing import Callable, Any, Tuple


def measure_memory(func: Callable) -> Callable:
    """
    A decorator that measures the memory usage of a function.
    Returns both the function result and memory usage statistics.
    
    Args:
        func: The function to measure memory usage for
        
    Returns:
        A wrapped function that returns (result, current_memory, peak_memory)
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Tuple[Any, float, float]:
        # Start memory tracing
        tracemalloc.start()
        
        # Execute function
        result = func(*args, **kwargs)
        
        # Get memory snapshot
        current, peak = tracemalloc.get_traced_memory()
        
        # Stop tracing
        tracemalloc.stop()
        
        # Convert to MB and return with result
        current_mb = current / 10**6
        peak_mb = peak / 10**6
        
        return result, current_mb, peak_mb
        
    return wrapper

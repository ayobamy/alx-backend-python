#!/usr/bin/env python3
"""
Measure the runtime
"""
import asyncio
import time


wait_random = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """
    measures the total execution time for wait_n
    """
    start = time.perf_counter()
    asyncio.run(wait_n(n, max_delay))
    total = time.perf_counter() - start_time

    return total

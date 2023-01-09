#!/usr/bin/env python3
"""
multiple coroutines with async
"""
from typing import List
import asyncio


wait_random = __import__('0-basic_async_syntax').wait_random
task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """
    execute multiple coroutines at the same time with async
    """
    result = await asyncio.gather(*(task_wait_random(max_delay)
                                    for _ in range(n)))

    for i in range(len(result)):
        for j in range(i+1, len(result)):
            if (result[i] > result[j]):
                result[i], result[j] = result[j], result[i]

    return result

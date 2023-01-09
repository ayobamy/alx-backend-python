#!/usr/bin/env python3
"""
synchronous function
"""
from typing import List


wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asynsio.Task:
    """
    a function `task_wait_random` that
    takes an integer `max_delay` and
    returns a asyncio.Task
    """
    Task = asyncio.create_task(wait_random(max_delay))

    return Task

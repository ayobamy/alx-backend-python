#!/usr/bin/env python3
"""
type-annotated function
"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
    a function that multiplies a float by multiplier.
    """

    def fn(n: float) -> float:
        """
        Multiply a float by a multiplier
        """
        return n * multiplier

    return fn

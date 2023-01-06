#!/usr/bin/env python3
"""
type-annotated function
"""
from typing import List


def sum_list(input_list: List[float]) -> float:
    """Sum list of float
    """
    sum = 0
    for item in input_list:
        sum += item

    return sum

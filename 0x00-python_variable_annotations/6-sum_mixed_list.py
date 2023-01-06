#!/usr/bin/env python3
"""
function annotation
"""
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """
    Sum float and int together
    and return float
    """
    return float(sum(mxd_lst))

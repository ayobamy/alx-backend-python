#!/usr/bin/env python3
"""
annotated function
"""
from typing import Tuple, Union


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """
    Convert str and int/float and
    return a tuple
    """
    return (k, v**2)

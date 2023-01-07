#!/usr/bin/env python3
"""
Duck types
"""
from typing import Any, Sequence, Tuple, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """
    duck-typed annotations
    """
    if lst:
        return lst[0]
    else:
        return None

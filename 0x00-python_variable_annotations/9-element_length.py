#!/usr/bin/env python3
"""
type-annotated function
"""
from typing import List, Sequence, Iterable, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """
    modify the function
    """
    return [(i, len(i)) for i in lst]

#!/usr/bin/env python3
"""
type annotations
"""
from typing import Any, Mapping, Sequence, Tuple, Union, TypeVar


T = TypeVar("T")


def safely_get_value(dct: Mapping,
                     key: Any, default: Union[T, None]) -> Union[Any, T]:
    """
    Safely get a value from a dictionary.
    if key in dct:
        return dct[key]
    else:
        return default
    """
    if key in dct:
        return dct[key]
    else:
        return default

#!/usr/bin/env python3
"""
unit testing
"""
import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """
    Implement the TestAccessNestedMap.test_access_nested_map
    method to test that the method returns what it is
    supposed to
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, result):
        """
        test access_nested_map with nested_map
        """
        res = access_nested_map(nested_map, path)
        self.assertEqual(res, result)

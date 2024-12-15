#!/usr/bin/env python3
"""
unit testing
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Test suite for GithubOrgClient
    """

    @parameterized.expand([
        ("google", ),
        ("abc", )
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value
        """
        mock_get_json.return_value = {"name": org_name}
        github_client = GithubOrgClient(org_name)

        result = github_client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

        self.assertEqual(result, {"name": org_name})

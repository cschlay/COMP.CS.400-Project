"""Tests all tokens defined in the instructions, also test invalid tokens."""
from typing import List
from unittest import TestCase

import sslexer


class TokenTest(TestCase):
    """Test all valid tokens."""

    def test_reserved_keywords(self):
        pass

    def test_ignored_characters(self):
        ignored_characters: List[str] = [" "]
        for char in ignored_characters:
            self.assertFalse(sslexer.tokenize_data(data=char), msg=char)

    def test_ignored_comment(self):
        self.assertFalse(sslexer.tokenize_data(data="...comment text..."))
        self.assertFalse(sslexer.tokenize_data(data="... ..."))
        self.assertFalse(sslexer.tokenize_data(data="......"))
        self.assertFalse(sslexer.tokenize_data(data="...comment ... inside comment ... ..."))


class InvalidTokenTest(TestCase):
    """Test some invalid tokens."""
    pass

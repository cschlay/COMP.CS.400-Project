"""Tests all tokens defined in the instructions, also test invalid tokens."""
from typing import List
from unittest import TestCase

import sslexer


class TokenTest(TestCase):
    """Test all valid tokens."""

    def test_token_assign(self):
        token = sslexer.tokenize_data(data=":=")[0]
        self.assertEqual(token.type, "ASSIGN")
        self.assertEqual(token.value, ":=")

    def test_token_curly_brackets(self):
        token = sslexer.tokenize_data(data="{")[0]
        self.assertEqual(token.type, "LCURLY")
        self.assertEqual(token.value, "{")
        token = sslexer.tokenize_data(data="}")[0]
        self.assertEqual(token.type, "RCURLY")
        self.assertEqual(token.value, "}")

    def test_token_equalities(self):
        token = sslexer.tokenize_data(data="=")[0]
        self.assertEqual(token.type, "EQ")
        self.assertEqual(token.value, "=")

        token = sslexer.tokenize_data(data="!=")[0]
        self.assertEqual(token.type, "NOTEQ")
        self.assertEqual(token.value, "!=")

        token = sslexer.tokenize_data(data="<")[0]
        self.assertEqual(token.type, "LT")
        self.assertEqual(token.value, "<")

        token = sslexer.tokenize_data(data="<=")[0]
        self.assertEqual(token.type, "LTEQ")
        self.assertEqual(token.value, "<=")

        token = sslexer.tokenize_data(data=">")[0]
        self.assertEqual(token.type, "GT")
        self.assertEqual(token.value, ">")

        token = sslexer.tokenize_data(data=">=")[0]
        self.assertEqual(token.type, "GTEQ")
        self.assertEqual(token.value, ">=")

    def test_token_ident(self):
        # Length just two.
        token = sslexer.tokenize_data(data=" ab")[0]
        self.assertEqual(token.type, "IDENT")
        self.assertEqual(token.value, "ab")

        # Length is much greater than two.
        token = sslexer.tokenize_data(data="the_length_is_much_greater_than_two")[0]
        self.assertEqual(token.type, "IDENT")
        self.assertEqual(token.value, "the_length_is_much_greater_than_two")

        # Contains invalid characters
        with self.assertRaises(Exception):
            sslexer.tokenize_data(data="öäöäö")

        # Starts with number
        with self.assertRaises(Exception):
            sslexer.tokenize_data(data="123956abs")

        # Length is too short.
        with self.assertRaises(Exception):
            sslexer.tokenize_data(data="a")

    def test_token_math(self):
        # Tests only math operators.
        token = sslexer.tokenize_data(data="+")[0]
        self.assertEqual(token.type, "PLUS")
        self.assertEqual(token.value, "+")

        token = sslexer.tokenize_data(data="-")[0]
        self.assertEqual(token.type, "MINUS")
        self.assertEqual(token.value, "-")

        token = sslexer.tokenize_data(data="*")[0]
        self.assertEqual(token.type, "MULT")
        self.assertEqual(token.value, "*")

        token = sslexer.tokenize_data(data="/")[0]
        self.assertEqual(token.type, "DIV")
        self.assertEqual(token.value, "/")

    def test_token_parenthesis(self):
        token = sslexer.tokenize_data(data="(")[0]
        self.assertEqual(token.type, "LPAREN")
        self.assertEqual(token.value, "(")
        token = sslexer.tokenize_data(data=")")[0]
        self.assertEqual(token.type, "RPAREN")
        self.assertEqual(token.value, ")")

    def test_token_square_brackets(self):
        token = sslexer.tokenize_data(data="[")[0]
        self.assertEqual(token.type, "LSQUARE")
        self.assertEqual(token.value, "[")
        token = sslexer.tokenize_data(data="]")[0]
        self.assertEqual(token.type, "RSQUARE")
        self.assertEqual(token.value, "]")

    def test_reserved_keywords(self):
        for keyword, token_type in sslexer.reserved.items():
            token = sslexer.tokenize_data(data=keyword)[0]
            self.assertEqual(token.type, token_type)
            self.assertEqual(token.value, keyword)

    def test_ignored_characters(self):
        ignored_characters: List[str] = [" "]
        for char in ignored_characters:
            self.assertFalse(sslexer.tokenize_data(data=char), msg=char)

    def test_ignored_comment(self):
        self.assertFalse(sslexer.tokenize_data(data="...comment text..."))
        self.assertFalse(sslexer.tokenize_data(data="... ..."))
        self.assertFalse(sslexer.tokenize_data(data="......"))
        self.assertFalse(sslexer.tokenize_data(data="...comment ... inside comment ... ..."))

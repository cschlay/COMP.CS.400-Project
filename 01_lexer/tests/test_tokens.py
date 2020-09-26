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

    def test_token_coordinate_ident(self):
        token = sslexer.tokenize_data(data="CL123")[0]
        self.assertEqual(token.type, "COORDINATE_IDENT")
        self.assertEqual(token.value, "CL123")

        # Other kind of allowed of correct variations.
        token = sslexer.tokenize_data(data="C123")[0]
        self.assertEqual(token.type, "COORDINATE_IDENT")
        self.assertEqual(token.value, "C123")

        token = sslexer.tokenize_data(data="C1")[0]
        self.assertEqual(token.type, "COORDINATE_IDENT")
        self.assertEqual(token.value, "C1")

        # Too many capital letters
        with self.assertRaises(Exception):
            sslexer.tokenize_data(data="CCC")

    def test_token_curly_brackets(self):
        token = sslexer.tokenize_data(data="{")[0]
        self.assertEqual(token.type, "LCURLY")
        self.assertEqual(token.value, "{")
        token = sslexer.tokenize_data(data="}")[0]
        self.assertEqual(token.type, "RCURLY")
        self.assertEqual(token.value, "}")

    def test_token_decimal_literal(self):
        # Positive decimal
        token = sslexer.tokenize_data(data="20.2")[0]
        self.assertEqual(token.type, "DECIMAL_LITERAL")
        self.assertEqual(token.value, "20.2")

        # Negative decimal
        token = sslexer.tokenize_data(data="-20.2")[0]
        self.assertEqual(token.type, "DECIMAL_LITERAL")
        self.assertEqual(token.value, "-20.2")

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

        # Length is too short.
        with self.assertRaises(Exception):
            print(sslexer.tokenize_data(data="a"))

    def test_info_string(self):
        token = sslexer.tokenize_data(data="!infostring!")[0]
        self.assertEqual(token.type, "INFO_STRING")
        self.assertEqual(token.value, "!infostring!")

    def test_int_literal(self):
        token = sslexer.tokenize_data(data="1234")[0]
        self.assertEqual(token.type, "INT_LITERAL")
        self.assertEqual(token.value, "1234")

        token = sslexer.tokenize_data(data="-1234")[0]
        self.assertEqual(token.type, "INT_LITERAL")
        self.assertEqual(token.value, "-1234")

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

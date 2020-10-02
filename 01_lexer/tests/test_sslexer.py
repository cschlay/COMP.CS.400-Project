from typing import List, Tuple
from unittest import TestCase

import ply

import sslexer
from main import read_file


class SSLexerTest(TestCase):
    def test_tokenize_data(self):
        expected_tokens: List[Tuple[str, str]] = [
            ("FUNCTION", "function"),
            ("FUNC_IDENT", "Update_index_fund"),
            ("LPAREN", "("),
            ("IDENT", "id"),
            ("RPAREN", ")"),
            ("COLON", ":"),
            ("IDENT", "index_fund"),
            ("ASSIGN", ":="),
            ("FUNC_IDENT", "Fetch_index_fund"),
            ("LPAREN", "("),
            ("IDENT", "id"),
            ("RPAREN", ")"),
            ("IDENT", "index_fund"),
            ("LSQUARE", "["),
            ("IDENT", "value"),
            ("RSQUARE", "]"),
            ("ASSIGN", ":="),
            ("IDENT", "index_fund"),
            ("LSQUARE", "["),
            ("IDENT", "value"),
            ("RSQUARE", "]"),
            ("MULT", "*"),
            ("DECIMAL_LITERAL", "1.1"),
            ("IF", "if"),
            ("INT_LITERAL", "3"),
            ("GTEQ", ">="),
            ("INT_LITERAL", "1"),
            ("COLON", ":"),
            ("FUNC_IDENT", "Post_data"),
            ("LPAREN", "("),
            ("LCURLY", "{"),
            ("SQUOTE", "'"),
            ("IDENT", "valueToday"),
            ("SQUOTE", "'"),
            ("COLON", ":"),
            ("INT_LITERAL", "180"),
            ("RCURLY", "}"),
            ("RPAREN", ")"),
            ("ENDIF", "endif"),
            ("END", "end")
        ]
        token_list: List[ply.lex.LexToken] = sslexer.tokenize_data(data=read_file('code.sheetscript'))
        for token, expected in zip(token_list, expected_tokens):
            self.assertEqual(token.type, expected[0], msg=token)
            self.assertEqual(token.value, expected[1], msg=token)

"""
Actual lexer implementation for SheetScript.
"""

from typing import Tuple

import ply.lex

tokens: Tuple[str, ...] = ("COMMENT", "WHITESPACE")

t_COMMENT: str = r'C'
t_WHITESPACE: str = r'W'


def t_error(t):
    """
    The required error handling for PLY.

    Raises a generic Exception with illegal character at given line.

    :param t: the token where error occurred
    """
    raise Exception(f"Illegal character '{t.value[0]}' at line { t.lexer.lineno}")


lexer: ply.lex.Lexer = ply.lex.lex()


def tokenize_data(data: str):
    """
    Performs the actual tokenization with PLY lexer.
    """
    lexer.input(data)
    for token in lexer:
        print(token)

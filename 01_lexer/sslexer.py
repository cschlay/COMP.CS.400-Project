"""
Actual lexer implementation for SheetScript.
"""

from typing import List, Tuple

import ply.lex

tokens: Tuple[str, ...] = ("COMMENT", "ASSIGN")

t_COMMENT: str = r"...."

# According to PLY docs, t_ignore is used for ignoring characters.
t_ignore: str = " \r"


def t_error(t):
    """
    The required error handling for PLY.

    Raises a generic Exception with illegal character at given line.

    :param t: the token where error occurred
    """
    raise Exception(f"Illegal character '{t.value[0]}' at line { t.lexer.lineno}")


lexer: ply.lex.Lexer = ply.lex.lex()


def tokenize_data(data: str) -> List[ply.lex.LexToken]:
    """
    Performs the actual tokenization with PLY lexer.

    :param data:
    :return: A list of LexToken instances.
    """
    lexer.input(data)

    print(list(lexer))
    token_list: List[ply.lex.LexToken] = []
    for token in lexer:
        token_list.append(token)

    return token_list

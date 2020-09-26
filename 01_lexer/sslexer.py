"""
Actual lexer implementation for SheetScript.

[1] Note to self, the token functions cannot have docstrings! The first line must be regular expression!
"""

from typing import Dict, List

import ply.lex

# Reserved keywords, recommended to not declared as token by docs 4.3..
# The docs showed an example of using dict but it might be simpler to just use list and map it if necessary.
# I have preserved the order given in the instructions in case the order matter later.
reserved_keywords: List[str] = [
    "scalar",
    "range",
    "do",
    "done",
    "is",
    "while",
    "for",
    "if",
    "then",
    "else",
    "endif",
    "function",
    "subroutine",
    "return",
    "end",
    "print_sheet",
    "print_scalar",
    "print_range"
]
reserved: Dict[str, str] = {word: word.upper() for word in reserved_keywords}

# Token definitions.
tokens: List[str] = ["COMMENT", "ASSIGN", "IDENT"] + list(reserved.values())

# The order for tokens are also preserved as given in case it matters.
t_ASSIGN: str = r":="


# Variable name definition. The length has to be at least one and not a reserved word.
def t_IDENT(t):
    r"[a-z]{1}[0-9A-Za-z_]+"
    t.type = reserved.get(t.value, "IDENT")
    return t


# According to PLY docs, t_ignore is used for ignoring characters and tokens.
t_ignore: str = " \r"
t_ignore_COMMENT: str = r"\.\.\..*\.\.\."


# Defines the newline and keeps track of it.
# The docs says that PLY doesn't know newlines by default.
def t_newline(t):
    r"\n"
    t.lexer.lineno += 1


def t_error(t):
    """
    The required error handling for PLY.
    Raises a generic Exception with illegal character at given line.

    :param t: the token where error occurred
    """
    raise Exception(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")


lexer: ply.lex.Lexer = ply.lex.lex()


def tokenize_data(data: str) -> List[ply.lex.LexToken]:
    """
    Performs the actual tokenization with PLY lexer.

    :param data:
    :return: A list of LexToken instances.
    """
    lexer.input(data)
    return list(lexer)

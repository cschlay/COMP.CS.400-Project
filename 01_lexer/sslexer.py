"""
Actual lexer implementation for SheetScript.

[1] Note to self, the token functions cannot have docstrings! The first line must be regular expression!
[2] Note for reader short notations such as \d in regular expressions are avoided if possible
to improve flexibility and readability.
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
tokens: List[str] = [
                        "COMMENT",
                        "ASSIGN",
                        # Brackets and parentheses
                        "LPAREN",
                        "RPAREN",
                        "LSQUARE",
                        "RSQUARE",
                        "LCURLY",
                        "RCURLY",
                        # Characters
                        "COMMA",
                        "DOTDOT",
                        "SQUOTE",
                        "COLON",
                        "DOLLAR",
                        "NUMBER_SIGN",
                        # Math
                        "EQ",
                        "NOTEQ",
                        "LT",
                        "LTEQ",
                        "GT",
                        "GTEQ",
                        "PLUS",
                        "MINUS",
                        "MULT",
                        "DIV",
                        # Long tokens
                        "INFO_STRING",
                        "COORDINATE_IDENT",
                        "DECIMAL_LITERAL",
                        "INT_LITERAL",
                        "IDENT",
                        "RANGE_IDENT",
                        "SHEET_IDENT",
                        "FUNC_IDENT"
                    ] + list(reserved.values())

# The order for tokens are also preserved as given in case it matters.
t_ASSIGN: str = r":="
# Parenthesis
t_LPAREN: str = r"\("
t_RPAREN: str = r"\)"
t_LSQUARE: str = r"\["
t_RSQUARE: str = r"\]"
t_LCURLY: str = r"\{"
t_RCURLY: str = r"\}"
# Characters
t_COMMA: str = r","
t_DOTDOT: str = r"\.\."
t_SQUOTE: str = r"\'"
t_COLON: str = r"\:"
t_DOLLAR: str = r"\$"
t_NUMBER_SIGN: str = r"\#"
# Math
t_EQ: str = r"="
t_NOTEQ: str = r"!="
t_LT: str = r"<"
t_LTEQ: str = r"<="
t_GT: str = r">"
t_GTEQ: str = r">="
t_PLUS: str = r"\+"
t_MINUS: str = r"-"
t_MULT: str = r"\*"
t_DIV: str = r"/"
# The long tokens
t_INFO_STRING: str = r"!.*!"  # It was not specified what characters are allowed.


# 1-2 capital letters and 1-3 digits
# Placed above t_IDENT to increase the precedence.
def t_COORDINATE_IDENT(t):
    r"[A-Z]{1,2}[0-9]{1,3}"
    return t


t_DECIMAL_LITERAL: str = r"(0\.[0-9]{1})|(-?[0-9]?[0-9]*\.[0-9]{1})"  # only one decimal
t_INT_LITERAL: str = r"0|-?[0-9^0]+"  # integers in traditional sense


# Variable name definition. The length has to be at least one and not a reserved word.
def t_IDENT(t):
    r"[a-z]{1}[0-9A-Za-z_]+"
    t.type = reserved.get(t.value, "IDENT")
    return t


t_RANGE_IDENT: str = r"_{1}[0-9A-Za-z_]+"  # just like IDENT but starts with underscore
t_SHEET_IDENT: str = r"[A-Z]+"  # capital letter only text
t_FUNC_IDENT: str = r"[A-Z]{1}[0-9a-z_]+"

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

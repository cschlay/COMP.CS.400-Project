"""
A helper to construct the AST.
"""
from typing import List


class Atom:
    def __init__(self, value: str, has_number_sign: bool = False, has_parenthesis: bool = False):
        self.value = value
        self.has_number_sign = has_number_sign
        self.has_parenthesis = has_parenthesis


class RangeDefinition:
    def __init__(self, name: str, value: str = None):
        self.name = name
        self.value = value


class ScalarDefinition:
    def __init__(self, name: str, value: str = None):
        self.name = name
        self.value = value


class SheetDefinition:
    def __init__(self, name: str, sheet_init=None):
        self.name = name

        # For unevaluated INT_LITERAL MULT INT_LITERAL
        self.sheet_init = sheet_init

"""
A helper to construct the AST.
"""
from typing import List, Union


class Program:
    def __init__(self, functions_and_variables: List = [], statements: List = []):
        self.functions_and_variables = functions_and_variables
        self.statements = statements


class Atom:
    def __init__(self, value: str, has_number_sign: bool = False, has_parenthesis: bool = False):
        self.value = value
        self.has_number_sign = has_number_sign
        self.has_parenthesis = has_parenthesis


class Factor:
    def __init__(self, value: str, has_minus: bool = False):
        self.value = value
        self.has_minus = has_minus


class Math:
    def __init__(self, op, *args):
        self.op = op
        self.values = args


class RangeDefinition:
    def __init__(self, name: str, value: str = None):
        self.name = name
        self.value = value


class ScalarDefinition:
    def __init__(self, name: str, value: str = None):
        self.name = name
        self.value = value


class SimpleExpression:
    def __init__(self, value, op: str=None, other_value=None):
        self.value = value
        self.op = op
        self.other_value = other_value


class SheetDefinition:
    def __init__(self, name: str, value=None):
        self.name = name
        self.value = value


class SheetInit:
    def __init__(self, value):
        self.value = value


class SheetInitList:
    def __init__(self, value: List):
        self.value = value


class SheetRow:
    def __init__(self, value):
        self.value = value


class Term:
    def __init__(self, value, op: str = None, other_value=None):
        self.value = value
        self.op = op
        self.other_value = other_value


class VariableDefinition:
    def __init__(self, value):
        self.name = value.name
        self.value = value

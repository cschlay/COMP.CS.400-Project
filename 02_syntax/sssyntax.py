"""
A helper to construct the AST.
"""


class RangeDefinition:
    def __init__(self, name: str, value: str = None):
        self.name = name
        self.value = value


class ScalarDefinition:
    def __init__(self, name: str, value: str = None):
        self.name = name
        self.value = value

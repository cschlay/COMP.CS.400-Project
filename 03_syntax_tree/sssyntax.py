"""
A helper to construct the AST.
"""

TYPE_ASSIGNMENT = "assignment"
TYPE_ATOM = "atom"
TYPE_CELL_REF = "cell_ref"
TYPE_COORDINATE_IDENT = "COORDINATE_IDENT"
TYPE_DECIMAL = "decimal"
TYPE_EXPRESSION = "expression"
TYPE_FOR = "for"
TYPE_FORMAL_ARG = "formal_arg"
TYPE_FUNCTION_CALL = "function_call"
TYPE_FUNCTION_DEFINITION = "function_definition"
TYPE_FUNC_IDENT = "FUNC_IDENT"
TYPE_IDENT = "IDENT"
TYPE_IF = "if"
TYPE_INFO_STRING = "info_string"
TYPE_INT = "int_literal"
TYPE_NAME = "name"
TYPE_OP = "op"
TYPE_PROGRAM = "program"
TYPE_RANGE_DEFINITION = "range_definition"
TYPE_RANGE_IDENT = "RANGE_IDENT"
TYPE_RANGE_EXPRESSION = "range_expression"
TYPE_RETURN_TYPE = "RETURN_TYPE"
TYPE_RETURN = "return"
TYPE_SCALAR = "scalar"
TYPE_SCALAR_DEFINITION = "scalar_definition"
TYPE_SCALAR_EXPRESSION = "scalar_expression"
TYPE_SHEET_DEFINITION = "sheet_definition"
TYPE_SHEET_IDENT = "SHEET_IDENT"
TYPE_SHEET_INIT = "sheet_init"
TYPE_SHEET_INIT_LIST = "sheet_init_list"
TYPE_SHEET_ROW = "sheet_row"
TYPE_SUBROUTINE_DEFINITION = "subroutine_definition"
TYPE_SUBROUTINE_CALL = "subroutine_call"
TYPE_TERM = "term"
TYPE_VARIABLE_DEFINITION ="variable_definition"


class Node:
    """
    The base node for every other nodes for AST inherits this.
    """

    def __init__(self, nodetype: str, value: str = None, **kwargs):
        self.nodetype: str = self._validate_nodetype(nodetype)
        if value is not None:
            self.value: str = value

        # Put the children as attributes.
        for attr, value in kwargs.items():
            setattr(self, attr, value)
            """
            if attr.startswith("children_") and type(value) is list:
                setattr(self, attr, value)
            elif attr.startswith("child_") and type(value) is Node:
                setattr(self, attr, value)
            else:
                raise TypeError(f"Invalid child node {attr}, the value is {value}.")
            """

    def _validate_nodetype(self, nodetype: str):
        #if nodetype not in [TYPE_PROGRAM, TYPE_VARIABLE_DEFINITION]:
        #     raise TypeError("Nodetype not implemented!")
        return nodetype

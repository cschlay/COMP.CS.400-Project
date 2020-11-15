"""
The syntax parser of SheetScript.
The order of grammar definition is preserved as given in specification.
"""
import decimal
from typing import List

import ply.yacc

import sslexer
import sssyntax as nodes

tokens: List[str] = sslexer.tokens

# Alias for p arg typehint for easier development.
P = [ply.yacc.YaccProduction]


def p_program(p: P):
    """program : multiple_function_or_variable_definition statement_list
               | statement_list"""
    if len(p) == 3:
        # multiple_function_or_variable_definition statement_list
        p[0] = nodes.Node(nodetype=nodes.TYPE_PROGRAM,
                          children_function_or_variable_definition=p[1],
                          children_statement_list=p[2])
    else:
        # statement_list
        p[0] = nodes.Node(nodetype=nodes.TYPE_PROGRAM, children_statement_list=p[1])


# Additional definition for multiple function_or_variable_defs, uses lists
def p_multiple_function_or_variable_definition(p: P):
    """multiple_function_or_variable_definition : function_or_variable_definition multiple_function_or_variable_definition
                                                | function_or_variable_definition"""
    if len(p) == 3:
        # multiple_function_or_variable_definition function_or_variable_definition
        p[0] = [p[1]] + p[2]
    else:
        # function_or_variable_definition
        p[0] = [p[1]]


def p_function_or_variable_definition(p: P):
    """function_or_variable_definition : variable_definition
                                       | function_definition
                                       | subroutine_definition"""
    # Omitted
    p[0] = p[1]


def p_variable_definition(p: P):
    """variable_definition : scalar_definition
                           | range_definition
                           | sheet_definition"""
    # Omitted
    p[0] = p[1]


def p_function_definition(p: P):
    """function_definition : FUNCTION FUNC_IDENT LSQUARE RSQUARE RETURN scalar_or_range IS statement_list END
                           | FUNCTION FUNC_IDENT LSQUARE formals RSQUARE RETURN scalar_or_range IS statement_list END
                           | FUNCTION FUNC_IDENT LSQUARE RSQUARE RETURN scalar_or_range IS multiple_variable_definition statement_list END
                           | FUNCTION FUNC_IDENT LSQUARE formals RSQUARE RETURN scalar_or_range IS multiple_variable_definition statement_list END"""
    # print(f"function_definition( {p[2]} )")
    p[0] = nodes.Node(nodetype=nodes.TYPE_FUNCTION_DEFINITION)


# helper definition for scalar or range in function
def p_scalar_or_range(p: P):
    """scalar_or_range : SCALAR
                       | RANGE"""
    # Omitted, since its just helper for function to check the syntax.
    p[0] = p[1]


# helper definition for multiple variables
def p_multiple_variable_definition(p: P):
    """multiple_variable_definition : variable_definition multiple_variable_definition
                                    | variable_definition"""
    if len(p) == 3:
        # variable_definition multiple_variable_definition
        p[0] = [p[1]] + p[2]
    else:
        # variable_definition
        p[0] = [p[1]]


def p_subroutine_definition(p: P):
    """subroutine_definition : SUBROUTINE FUNC_IDENT LSQUARE RSQUARE IS multiple_variable_definition statement_list END
                             | SUBROUTINE FUNC_IDENT LSQUARE formals RSQUARE IS multiple_variable_definition statement_list END"""
    length: int = len(p)
    if length == 9:
        # without formals
        p[0] = nodes.Node(
            nodetype=nodes.TYPE_SUBROUTINE_DEFINITION,
            child_name=nodes.Node(nodetype=nodes.TYPE_FUNC_IDENT),
            children_variable_definitions=p[6],
            children_statement_list=p[7]
        )
    else:
        # with formals
        p[0] = nodes.Node(
            nodetype=nodes.TYPE_SUBROUTINE_DEFINITION,
            child_name=nodes.Node(nodetype=nodes.TYPE_FUNC_IDENT),
            children_variable_definitions=p[7],
            children_statement_list=p[8]
        )


def p_formals(p: P):
    """formals : formal_arg COMMA formal_arg
               | formal_arg"""
    pass


def p_formal_arg(p: P):
    """formal_arg : IDENT COLON SCALAR
                  | RANGE_IDENT COLON RANGE
                  | SHEET_IDENT COLON SHEET"""
    pass


def p_sheet_definition(p: P):
    """sheet_definition : SHEET SHEET_IDENT sheet_init
                        | SHEET SHEET_IDENT
    """
    if len(p) == 4:
        # SHEET SHEET_IDENT sheet_init
        p[0] = nodes.Node(
            nodetype=nodes.TYPE_SHEET_DEFINITION,
            child_name=nodes.Node(nodetype="SHEET_INIT", value=p[2]),
            child_sheet_init=p[3]
        )
    else:
        # SHEET SHEET_IDENT
        p[0] = nodes.Node(
            nodetype=nodes.TYPE_SHEET_DEFINITION,
            child_name=nodes.Node(nodetype="SHEET_INIT", value=p[2]),
        )


def p_sheet_init(p: P):
    """sheet_init : EQ sheet_init_list
                  | EQ INT_LITERAL MULT INT_LITERAL
    """
    if len(p) == 3:
        # EQ sheet_init_list
        p[0] = nodes.Node(nodetype=nodes.TYPE_SHEET_INIT, children_sheet_init_list=p[2])
    else:
        # EQ INT_LITERAL MULT INT_LITERAL
        p[0] = nodes.Node(
            nodetype=nodes.TYPE_OP,
            value=p[3],
            child_left=nodes.Node(nodetype=nodes.TYPE_INT, value=p[2]),
            child_right=nodes.Node(nodetype=nodes.TYPE_INT, value=p[4])
        )


def p_sheet_init_list(p: P):
    """sheet_init_list : LCURLY multiple_sheet_row RCURLY"""
    p[0] = p[2]


def p_multiple_sheet_row(p: P):
    """multiple_sheet_row : sheet_row multiple_sheet_row
                          | sheet_row"""
    length: int = len(p)
    if length == 3:
        # sheet_row {sheet_row}
        p[0] = [p[1]] + p[2]
    elif length == 2:
        # sheet_row
        p[0] = [p[1]]


def p_sheet_row(p: P):
    """sheet_row : simple_expr COMMA sheet_row
                 | simple_expr"""
    length: int = len(p)
    if length == 4:
        # simple_expr { COMMA simple_expr }
        if hasattr(p[3], "children_simple_expr"):
            p[0] = nodes.Node(nodetype=nodes.TYPE_SHEET_ROW, children_simple_expr=[p[1], *p[3].children_simple_expr])
        else:
            p[0] = nodes.Node(nodetype=nodes.TYPE_SHEET_ROW, children_simple_expr=[p[1], p[3].child_])
    elif length == 2:
        # simple_expr
        p[0] = nodes.Node(nodetype=nodes.TYPE_SHEET_ROW, child_=p[1])


def p_range_definition(p: P):
    """range_definition : RANGE RANGE_IDENT EQ range_expr
                        | RANGE RANGE_IDENT"""
    if len(p) == 5:
        # RANGE RANGE_IDENT EQ range_expr
        p[0] = nodes.Node(
            nodetype=nodes.TYPE_RANGE_DEFINITION,
            child_name=nodes.Node(nodetype=nodes.TYPE_RANGE_IDENT, value=p[2]),
            child_expression=p[4]
        )
    elif len(p) == 3:
        # RANGE RANGE_IDENT
        p[0] = nodes.Node(
            nodetype=nodes.TYPE_RANGE_DEFINITION,
            child_name=nodes.Node(nodetype=nodes.TYPE_RANGE_IDENT, value=p[2]),
        )


def p_scalar_definition(p: P):
    """scalar_definition : SCALAR IDENT EQ scalar_expr
                         | SCALAR IDENT"""
    if len(p) == 5:
        # SCALAR IDENT EQ scalar_expr
        p[0] = nodes.Node(
            nodetype=nodes.TYPE_SCALAR_DEFINITION,
            child_name=nodes.Node(nodetype=nodes.TYPE_SCALAR, value=p[2]),
            child_expression=p[4]
        )
    elif len(p) == 3:
        # SCALAR IDENT
        p[0] = nodes.Node(
            nodetype=nodes.TYPE_SCALAR_DEFINITION,
            child_name=nodes.Node(nodetype=nodes.TYPE_SCALAR, value=p[2]),
        )



def p_statement_list(p: P):
    """statement_list : statement statement_list
                      | statement"""
    length: int = len(p)
    if length == 3:
        # statement {statement}
        p[0] = [p[1]] + p[2]
    else:
        # statement
        p[0] = [p[1]]


def p_statement(p: P):
    """statement : PRINT_SHEET SHEET_IDENT
                 | PRINT_SHEET INFO_STRING SHEET_IDENT
                 | PRINT_RANGE range_expr
                 | PRINT_RANGE INFO_STRING range_expr
                 | PRINT_SCALAR scalar_expr
                 | PRINT_SCALAR INFO_STRING scalar_expr
                 | IF scalar_expr THEN statement_list ENDIF
                 | IF scalar_expr THEN statement_list ELSE statement_list ENDIF
                 | WHILE scalar_expr DO statement_list DONE
                 | FOR range_list DO statement_list DONE
                 | subroutine_call
                 | RETURN scalar_expr
                 | RETURN range_expr
                 | assignment"""
    length: int = len(p)
    if p[1] in ["print_sheet", "print_range", "print_scalar"]:
        # PRINT_SHEET [INFO_STRING] SHEET_IDENT
        # PRINT_RANGE [INFO_STRING] range_expr
        # PRINT_SCALAR [INFO_STRING] scalar_expr
        if len(p) == 4:
            # has info string
            if type(p[3]) is nodes.Node:
                # range_expr or scalar_expr
                p[0] = nodes.Node(
                    nodetype=p[1],
                    child_info_string=nodes.Node(nodetype=nodes.TYPE_INFO_STRING, value=p[2]),
                    child_expression=p[3]
                )
            else:
                # sheet_ident
                p[0] = nodes.Node(
                    nodetype=p[1],
                    child_info_string=nodes.Node(nodetype=nodes.TYPE_INFO_STRING, value=p[2]),
                    child_name=nodes.Node(nodetype=nodes.TYPE_SHEET_IDENT, value=p[3])
                )
        else:
            # without info string
            if type(p[2]) is nodes.Node:
                p[0] = nodes.Node(nodetype=p[1], child_expression=p[2])
            else:
                p[0] = nodes.Node(nodetype=p[1], child_name=nodes.Node(nodetype=nodes.TYPE_SHEET_IDENT, value=p[2]))
    elif p[1] == "if":
        # IF scalar_expr THEN statement_list [ELSE statement_list] ENDIF
        if length == 6:
            p[0] = nodes.Node(
                nodetype=nodes.TYPE_IF,
                child_condition=p[2],
                children_then_statement_list=p[4]
            )
        elif length == 8:
            # with else
            p[0] = nodes.Node(
                nodetype=nodes.TYPE_IF,
                child_condition=p[2],
                children_then_statement_list=p[4],
                children_else_statement_list=p[6]
            )
    elif p[1] == "while":
        # WHILE scalar_expr DO statement_list DONE
        p[0] = nodes.Node(nodetype=nodes.TYPE_IF, children_condition=p[2], children_statement_list=p[4])
    elif p[1] == "for":
        # FOR range_list DO statement_list DONE
        p[0] = nodes.Node(nodetype=nodes.TYPE_FOR, children_range_list=p[2], children_statement_list=p[4])
    elif p[1] == "return":
        # RETURN scalar_expr
        # RETURN range_expr
        p[0] = nodes.Node(nodetype=nodes.TYPE_RETURN, child_expression=p[2])
    else:
        # assignment, subroutine_call
        p[0] = p[1]


def p_range_list(p: P):
    """range_list : range_expr COMMA range_list
                  | range_expr"""
    length: int = len(p)
    if length == 4:
        # range_expr { COMMA range_expr }
        p[0] = [p[1]] + p[3]
    elif length == 2:
        # range_expr
        p[0] = [p[1]]


def p_arguments(p: P):
    """arguments : arg_expr COMMA arg_expr
                 | arg_expr"""
    if len(p) == 4:
        # arg_expr COMMA arg_expr
        if type(p[1]) is list and type(p[3]) is list:
            p[0] = p[1] + p[3]
        elif type(p[1]) is list and type(p[3]) is not list:
            p[0] = p[1] + [p[3]]
        elif type(p[1]) is not list and type(p[3]) is list:
            p[0] = [p[1]] + p[3]
        else:
            p[0] = [p[1], p[3]]
    else:
        # arg_expr
        p[0] = [p[1]]


def p_arg_expr(p: P):
    """arg_expr : scalar_expr
                | range_expr
                | SHEET_IDENT"""
    if type(p[1]) == nodes.Node:
        # scalar_expr or range_expr
        p[0] = p[1]
    else:
        # SHEET IDENT
        p[0] = nodes.Node(nodetype=nodes.TYPE_SHEET_IDENT, value=p[1])


def p_subroutine_call(p: P):
    """subroutine_call : FUNC_IDENT LSQUARE arguments RSQUARE
                       | FUNC_IDENT LSQUARE RSQUARE"""
    length: int = len(p)
    if length == 5:
        # with arguments
        p[0] = nodes.Node(
            nodetype=nodes.TYPE_SUBROUTINE_CALL,
            child_name=nodes.Node(nodetype=nodes.TYPE_FUNC_IDENT, value=p[1]),
            children_arguments=p[3]
        )
    else:
        # without arguments
        p[0] = nodes.Node(
            nodetype=nodes.TYPE_SUBROUTINE_CALL,
            child_name=nodes.Node(nodetype=nodes.TYPE_FUNC_IDENT, value=p[1])
        )


def p_assignment(p: P):
    """assignment : IDENT ASSIGN scalar_expr
                  | cell_ref ASSIGN scalar_expr
                  | RANGE_IDENT ASSIGN range_expr
                  | SHEET_IDENT ASSIGN SHEET_IDENT"""
    if type(p[1]) is nodes.Node:
        # cell_ref ASSIGN scalar_expr
        p[0] = nodes.Node(
            nodetype=nodes.TYPE_ASSIGNMENT,
            child_cell_ref=p[1],
            child_expression=p[3]
        )
    elif type(p[3]) is not nodes.Node:
        # SHEET_IDENT ASSIGN SHEET_IDENT
        p[0] = nodes.Node(
            nodetype=nodes.TYPE_ASSIGNMENT,
            child_name=nodes.Node(nodetype=nodes.TYPE_SHEET_IDENT, value=p[1]),
            child_sheet_ident=nodes.Node(nodetype=nodes.TYPE_SHEET_IDENT, value=p[3])
        )
    elif p[3].nodetype == nodes.TYPE_RANGE_EXPRESSION:
        # RANGE_IDENT ASSIGN range_expr
        p[0] = nodes.Node(
            nodetype=nodes.TYPE_ASSIGNMENT,
            child_name=nodes.Node(nodetype=nodes.TYPE_RANGE_IDENT, value=p[1]),
            child_expression=p[3]
        )
    else:
        # IDENT ASSIGN scalar_expr
        p[0] = nodes.Node(
            nodetype=nodes.TYPE_ASSIGNMENT,
            child_name=nodes.Node(nodetype=nodes.TYPE_IDENT, value=p[1]),
            child_expression=p[3]
        )


def p_range_expr(p: P):
    """range_expr : RANGE_IDENT
                  | RANGE cell_ref DOTDOT cell_ref
                  | LSQUARE function_call RSQUARE
                  | range_expr LSQUARE INT_LITERAL COMMA INT_LITERAL RSQUARE"""
    length: int = len(p)
    if length == 2:
        # RANGE_IDENT, should be a reference
        p[0] = nodes.Node(nodes.TYPE_RANGE_IDENT, value=p[1])
    elif length == 5:
        # RANGE cell_ref DOTDOT cell_ref
        p[0] = nodes.Node(nodetype=nodes.TYPE_RANGE_EXPRESSION, child_from=p[2], child_to=p[4])
    elif length == 4:
        # LSQUARE function_call RSQUARE
        p[0] = p[2]
    elif length == 7:
        # range_expr LSQUARE INT_LITERAL COMMA INT_LITERAL RSQUARE
        p[0] = nodes.Node(
            nodetype=nodes.TYPE_RANGE_EXPRESSION,
            child_expression=p[1],
            child_from=nodes.Node(nodetype=nodes.TYPE_INT, value=p[3]),
            child_to=nodes.Node(nodetype=nodes.TYPE_INT, value=p[5])
        )


def p_cell_ref(p: P):
    """cell_ref : SHEET_IDENT SQUOTE COORDINATE_IDENT
                | DOLLAR COLON RANGE_IDENT
                | DOLLAR
    """
    length: int = len(p)
    if length == 4:
        if p[1] == "$":
            # DOLLAR COLON RANGE_IDENT
            p[0] = nodes.Node(
                nodetype=nodes.TYPE_CELL_REF,
                child_range_ident=nodes.Node(nodetype=nodes.TYPE_RANGE_IDENT, value=p[3])
            )
        else:
            # SHEET_IDENT SQUOTE COORDINATE_IDENT
            p[0] = nodes.Node(
                nodetype=nodes.TYPE_CELL_REF,
                child_sheet_ident=nodes.Node(nodetype=nodes.TYPE_SHEET_IDENT, value=p[1]),
                child_coordinate_ident=nodes.Node(nodetype=nodes.TYPE_COORDINATE_IDENT, value=p[3])
            )
    elif length == 2:
        # DOLLAR
        # should it be empty?
        p[0] = nodes.Node(nodetype=nodes.TYPE_CELL_REF, value=p[1])


def p_scalar_expr(p: P):
    """scalar_expr : simple_expr scalar_op scalar_expr
                   | simple_expr"""
    length: int = len(p)
    if length == 4:
        # simple_expr scalar_op scalar_expr
        p[0] = nodes.Node(nodetype=nodes.TYPE_OP, value=p[2], child_left=p[1], child_right=p[3])
    elif length == 2:
        # simple_expr
        p[0] = p[1]


# helper rule for scalar expr
def p_scalar_op(p: P):
    """scalar_op : EQ
                 | NOTEQ
                 | LT
                 | LTEQ
                 | GT
                 | GTEQ"""
    p[0] = p[1]


def p_simple_expr(p: P):
    """simple_expr : term PLUS simple_expr
                   | term MINUS simple_expr
                   | term"""
    if len(p) == 4:
        # term {(PLUS|MINUS) term}
        p[0] = nodes.Node(nodetype=nodes.TYPE_OP, value=p[2], child_left=p[1], child_right=p[3])
    elif len(p) == 2:
        # term
        p[0] = p[1]


def p_term(p: P):
    """term : factor MULT term
            | factor DIV term
            | factor"""
    if len(p) == 4:
        # factor {(MULT | DIV) factor}
        p[0] = nodes.Node(nodetype=nodes.TYPE_OP, value=p[2], child_left=p[1], child_right=p[3])
    elif len(p) == 2:
        # factor
        p[0] = p[1]


def p_factor(p: P):
    """factor : MINUS atom
              | atom"""
    if len(p) == 3:
        # MINUS atom
        p[0] = nodes.Node(nodetype=nodes.TYPE_OP, value=p[1], child_right=p[2])
    elif len(p) == 2:
        # atom
        p[0] = p[1]


def p_atom(p: P):
    """atom : IDENT
            | DECIMAL_LITERAL
            | function_call
            | cell_ref
            | NUMBER_SIGN range_expr
            | LPAREN scalar_expr RPAREN
    """
    if len(p) == 2:
        # IDENT, DECIMAL_LITERAL, function_call, cell_ref
        if type(p[1]) == str:
            # IDENT or DECIMAL_LITERAL
            try:
                # decimal_literal
                p[0] = nodes.Node(nodetype=nodes.TYPE_DECIMAL, value=decimal.Decimal(p[1]))
            except decimal.InvalidOperation:
                # ident
                p[0] = nodes.Node(nodetype=nodes.TYPE_IDENT, value=p[1])
        else:
            # function_call or cell_ref
            p[0] = p[1]
    elif (len(p)) == 3:
        # NUMBER_SIGN range_expr
        p[0] = p[1]
    elif (len(p)) == 4:
        # LPAREN scalar_expr RPAREN
        p[0] = p[1]


def p_function_call(p: P):
    """function_call : FUNC_IDENT LSQUARE arguments RSQUARE
                     | FUNC_IDENT LSQUARE RSQUARE"""

    if len(p) == 4:
        # FUNC_IDENT LSQUARE RSQUARE
        p[0] = nodes.Node(
            nodetype=nodes.TYPE_FUNCTION_CALL,
            child_name=nodes.Node(nodetype=nodes.TYPE_FUNC_IDENT, value=p[1]),
        )
    else:
        # With args
        p[0] = nodes.Node(
            nodetype=nodes.TYPE_FUNCTION_CALL,
            child_name=nodes.Node(nodetype=nodes.TYPE_FUNC_IDENT, value=p[1]),
            children_arguments=p[3]
        )


def p_error(p: P):
    print(f"{p.lineno}:Syntax Error (token:'{p.value}')")
    raise SystemExit


parser: ply.yacc.LRParser = ply.yacc.yacc()


def parse_data(data: str):
    """
    Returns the root of the abstract syntax tree.
    """
    return parser.parse(data, lexer=sslexer.lexer, debug=False)

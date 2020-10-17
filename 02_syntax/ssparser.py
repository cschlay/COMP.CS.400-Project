"""
The syntax parser of SheetScript.
The order of grammar definition is preserved as given in specification.
"""

from typing import List

import ply.yacc

import sslexer
import sssyntax as nodes

tokens: List[str] = sslexer.tokens

# Alias for p arg typehint for easier development.
P = [ply.yacc.YaccProduction]


def p_program(p: P):
    """program : multiple_function_or_variable_definition statement_list
               | function_or_variable_definition"""
    # No being sure how this will be used, it remains as dict.
    p[0] = nodes.Program(functions_and_variables=p[1])
    if len(p) == 3:
        p[0].statements = p[2]


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
    """
    # TODO: function_definition and subroutine_definition.
    p[0] = p[1]


def p_variable_definition(p: P):
    """variable_definition : scalar_definition
                           | range_definition
                           | sheet_definition
    """
    rule_type = type(p[1])
    p[0] = nodes.VariableDefinition(p[1])

    print_type: str = ""
    if rule_type is nodes.ScalarDefinition:
        print_type = "scalar"
    elif rule_type is nodes.RangeDefinition:
        print_type = "range"
    elif rule_type is nodes.SheetDefinition:
        print_type = "sheet"
    print(f"variable_definition({p[1].name}:{print_type})")


# p_function_definition
# p_subroutine_definition

# p_formals(p: P):
# p_formal_arg(p: P):


def p_sheet_definition(p: P):
    """sheet_definition : SHEET SHEET_IDENT sheet_init
                        | SHEET SHEET_IDENT
    """
    if len(p) == 4:
        # SHEET SHEET_IDENT sheet_init
        p[0] = nodes.SheetDefinition(name=p[2], value=p[3])
    else:
        # SHEET SHEET_IDENT
        p[0] = nodes.SheetDefinition(name=p[2])


def p_sheet_init(p: P):
    """sheet_init : EQ sheet_init_list
                  | EQ INT_LITERAL MULT INT_LITERAL
    """
    if type(p[2]) is list:
        # EQ sheet_init_list
        p[0] = nodes.SheetInit(p[2])
    else:
        # EQ INT_LITERAL MULT INT_LITERAL
        p[0] = nodes.SheetInit(nodes.Math(p[3], p[2], p[4]))


def p_sheet_init_list(p: P):
    """sheet_init_list : LCURLY multiple_sheet_row RCURLY"""
    p[0] = p[2]


# additional rule to allow multiple sheet_rows
# doesn't do it with class but a list of sheet rows
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
    if length == 5:
        # simple_expr { COMMA simple_expr }
        p[0] = nodes.SheetRow([p[1]] + p[3].value)
    elif length == 2:
        # simple_expr
        p[0] = nodes.SheetRow([p[1]])


def p_range_definition(p: P):
    """range_definition : RANGE RANGE_IDENT EQ range_expr
                        | RANGE RANGE_IDENT"""
    if len(p) == 5:
        # RANGE RANGE_IDENT EQ range_expr
        p[0] = nodes.RangeDefinition(name=p[2], value=p[4])
    elif len(p) == 3:
        # RANGE RANGE_IDENT
        p[0] = nodes.RangeDefinition(name=p[2])


def p_scalar_definition(p: P):
    """scalar_definition : SCALAR IDENT EQ scalar_expr
                         | SCALAR IDENT"""
    if len(p) == 5:
        # SCALAR IDENT EQ scalar_expr
        p[0] = nodes.ScalarDefinition(name=p[2], value=p[4])
    elif len(p) == 3:
        # SCALAR IDENT
        p[0] = nodes.ScalarDefinition(name=p[2])


# Uses Python list
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
                 | RETURN scalar_expr
                 | RETURN range_expr
                 | assignment"""
    # TODO: subroutine_call
    statement_name = None
    length: int = len(p)
    if p[1] in ["print_sheet", "print_range", "print_scalar"]:
        # PRINT_SHEET [INFO_STRING] SHEET_IDENT
        # PRINT_RANGE [INFO_STRING] range_expr
        # PRINT_SCALAR [INFO_STRING] scalar_expr
        p[0] = nodes.StatementPrint(p[1:])
    elif p[1] == "if":
        # IF scalar_expr THEN statement_list [ELSE statement_list] ENDIF
        if length == 5:
            p[0] = nodes.StatementIf(condition=p[2], if_statement_list=p[4])
        elif length == 7:
            # with else
            p[0] = nodes.StatementIf(condition=p[2], if_statement_list=p[4], else_statement_list=p[6])
    elif p[1] == "while":
        # WHILE scalar_expr DO statement_list DONE
        p[0] = nodes.StatementWhile(condition=p[2], statement_list=p[3])
    elif p[1] == "for":
        # FOR range_list DO statement_list DONE
        p[0] = nodes.StatementFor(range_list=p[1], statement_list=p[2])
    elif p[1] == "return":
        # RETURN scalar_expr
        # RETURN range_expr
        p[0] = nodes.StatementReturn(expression=p[2])
    elif type(p[1]) is nodes.Assignment:
        # assignment
        p[0] = nodes.Statement(p[1])
    # TODO: Verify "statement name" from the staff.
    print(f"statement({p[1]})")


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

# arguments
# p_arg_expr
# p_subroutine_call


def p_assignment(p: P):
    """assignment : IDENT ASSIGN scalar_expr
                  | cell_ref ASSIGN scalar_expr
                  | RANGE_IDENT ASSIGN range_expr
                  | SHEET_IDENT ASSIGN SHEET_IDENT"""
    p[0] = nodes.Assignment(variable=p[1], value=p[3])
    print(f"assignment({p[1]})")


def p_range_expr(p: P):
    """range_expr : RANGE_IDENT
                  | RANGE cell_ref DOTDOT cell_ref
                  | range_expr LSQUARE INT_LITERAL COMMA INT_LITERAL RSQUARE"""
    # TODO: LSQUARE function_call RSQUARE
    length: int = len(p)
    if length == 2:
        # RANGE_IDENT, should be a reference
        p[0] = nodes.RangeExpression(range_ident=p[1])
    elif length == 5:
        # RANGE cell_ref DOTDOT cell_ref
        p[0] = nodes.RangeExpression(cell1=p[2], cell2=p[4])
    elif length == 6:
        # range_expr LSQUARE INT_LITERAL COMMA INT_LITERAL RSQUARE
        p[0] = nodes.RangeExpression(range_expression=p[1], int_range1=p[3], int_range2=p[5])


def p_cell_ref(p: P):
    """cell_ref : SHEET_IDENT SQUOTE COORDINATE_IDENT
                | DOLLAR COLON RANGE_IDENT
                | DOLLAR
    """
    length: int = len(p)
    if length == 3:
        # SHEET_IDENT SQUOTE COORDINATE_IDENT
        if p[1] == "$":
            p[0] = nodes.CellRef(f"{p[1]}{p[2]}{p[3]}", range_ident=p[3], has_dollar=True)
        else:
            p[0] = nodes.CellRef(f"{p[1]}{p[2]}{p[3]}", sheet_ident=p[1], coordinate_ident=True)
    elif length == 1:
        p[0] = nodes.CellRef(p[1], has_dollar=True)


def p_scalar_expr(p: P):
    """scalar_expr : simple_expr scalar_op scalar_expr
                   | simple_expr"""
    print("scalar_expr")
    length: int = len(p)
    if length == 3:
        p[0] = nodes.ScalarExpression(p[1], op=p[2], other_value=p[3])
    elif length == 2:
        p[0] = nodes.ScalarExpression(p[1])


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
        # term {(PLUS|MINUS)} term
        p[0] = nodes.SimpleExpression(p[1], op=p[2], other_value=p[3])
    elif len(p) == 2:
        # term
        p[0] = nodes.SimpleExpression(p[1])


def p_term(p: P):
    """term : factor MULT term
            | factor DIV term
            | factor"""
    print("term")
    if len(p) == 4:
        # factor {(MULT | DIV)} factor
        p[0] = nodes.Term(p[1], op=p[2], other_value=p[3])
    elif len(p) == 2:
        # factor
        p[0] = nodes.Term(p[1])


def p_factor(p: P):
    """factor : MINUS atom
              | atom"""
    print("factor")
    if len(p) == 3:
        # MINUS atom
        p[0] = nodes.Factor(p[2], has_minus=True)
    elif len(p) == 1:
        # atom
        p[0] = nodes.Factor(p[1])


def p_atom(p: P):
    """atom : IDENT
            | DECIMAL_LITERAL
            | cell_ref
            | NUMBER_SIGN range_expr
            | LPAREN scalar_expr RPAREN
    """
    # TODO: function_call
    print("atom")
    if len(p) == 2:
        # IDENT, DECIMAL_LITERAL, cell_ref
        p[0] = nodes.Atom(p[1])
    elif (len(p)) == 3:
        # NUMBER_SIGN range_expr
        p[0] = nodes.Atom(p[2], has_number_sign=True)
    elif (len(p)) == 4:
        # LPAREN scalar_expr RPAREN
        p[0] = nodes.Atom(p[3], has_parenthesis=True)

# p_function_call


def p_error(p: P):
    print(f"{p.lineno}:Syntax Error (token:'{p.value}')")
    raise SystemExit


parser: ply.yacc.LRParser = ply.yacc.yacc()


def parse_data(data: str):
    parser.parse(data, lexer=sslexer.lexer, debug=False)

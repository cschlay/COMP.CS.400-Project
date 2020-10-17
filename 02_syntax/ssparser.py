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
    """program : function_or_variable_definition statement_list
               | function_or_variable_definition"""
    # TODO: {function_or_variable_definition}
    pass


def p_function_or_variable_definition(p: P):
    """function_or_variable_definition : variable_definition
    """
    # TODO: function_definition and subroutine_definition.
    pass


def p_variable_definition(p: P):
    """variable_definition : scalar_definition
                           | range_definition
                           | sheet_definition
    """
    p[0] = p[1]
    print_type: str = ''
    if type(p[0]) is nodes.ScalarDefinition:
        print_type = "scalar"
    elif type(p[0]) is nodes.RangeDefinition:
        print_type = "range"
    elif type(p[0]) is nodes.SheetDefinition:
        print_type = "sheet"
    print(f"variable_definition({p[0].name}:{print_type})")


# p_function_definition
# p_subroutine_definition

# p_formals(p: P):
# p_formal_arg(p: P):


def p_sheet_definition(p: P):
    """sheet_definition : SHEET SHEET_IDENT sheet_init
                        | SHEET SHEET_IDENT
    """
    if len(p) == 3:
        p[0] = nodes.SheetDefinition(name=p[2])
    else:
        p[0] = nodes.SheetDefinition(name=p[3])


def p_sheet_init(p: P):
    """sheet_init : EQ sheet_init_list
                  | EQ INT_LITERAL MULT INT_LITERAL
    """
    pass


def p_sheet_init_list(p: P):
    """sheet_init_list : LCURLY sheet_row RCURLY"""
    # TODO: LCURLY sheet_row { sheet_row } RCURLY
    pass


def p_sheet_row(p: P):
    """sheet_row : simple_expr COMMA sheet_row
                 | simple_expr"""
    length: int = len(p)
    if length == 5:
        # simple_expr { COMMA simple_expr }
        p[0] = nodes.SheetRow(p[1], op=p[2], other_value=p[3])
    elif length == 2:
        # simple_expr
        p[0] = nodes.SheetRow(p[1])


def p_range_definition(p: P):
    """range_definition : RANGE RANGE_IDENT EQ range_expr
                        | RANGE RANGE_IDENT"""
    if len(p) == 3:
        p[0] = nodes.RangeDefinition(name=p[2])
    elif len(p) == 5:
        p[0] = nodes.RangeDefinition(name=p[2], value=p[4])


def p_scalar_definition(p: P):
    """scalar_definition : SCALAR IDENT EQ scalar_expr
                         | SCALAR IDENT"""
    if len(p) == 3:
        p[0] = nodes.ScalarDefinition(name=p[2])
    elif len(p) == 5:
        p[0] = nodes.ScalarDefinition(name=p[2], value=p[4])


def p_statement_list(p: P):
    """statement_list : statement
                      | statement_list"""
    pass


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
    # TODO: Verify "statement name" from the staff.
    #if p[1] == 'print_sheet':
    #     statement_name = 'statement'
    print(f"statement({p[1]})")


def p_range_list(p: P):
    """range_list : range_expr"""
    # TODO: { COMMA range_expr }
    pass


# arguments
# p_arg_expr
# p_subroutine_call


def p_assignment(p: P):
    """assignment : IDENT ASSIGN scalar_expr
                  | cell_ref ASSIGN scalar_expr
                  | RANGE_IDENT ASSIGN range_expr
                  | SHEET_IDENT ASSIGN SHEET_IDENT"""
    pass


def p_range_expr(p: P):
    """range_expr : RANGE_IDENT
                  | RANGE cell_ref DOTDOT cell_ref
                  | range_expr LSQUARE INT_LITERAL COMMA INT_LITERAL RSQUARE"""
    # TODO: LSQUARE function_call RSQUARE
    pass


def p_cell_ref(p: P):
    """cell_ref : SHEET_IDENT SQUOTE COORDINATE_IDENT
                | DOLLAR COLON RANGE_IDENT
                | DOLLAR
    """
    print(p[0])


def p_scalar_expr(p: P):
    """scalar_expr : simple_expr"""
    # TODO: { (EQ|NOTEQ|LT|LTEQ|GT|GTEQ) simple_expr}
    pass


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
    print('term')
    if len(p) == 4:
        # factor {(MULT | DIV)} factor
        p[0] = nodes.Term(p[1], op=p[2], other_value=p[3])
    elif len(p) == 2:
        # factor
        p[0] = nodes.Term(p[1])


def p_factor(p: P):
    """factor : MINUS atom
              | atom"""
    print('factor')
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
    print('atom')
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

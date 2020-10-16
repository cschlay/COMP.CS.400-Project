from typing import List

import ply.yacc

import sslexer

tokens: List[str] = sslexer.tokens

# Alias for p arg typehint for easier development.
P = [ply.yacc.YaccProduction]


def p_program(p: P):
    """program : statement_list"""
    pass


def p_statement_list(p: P):
    """statement_list : statement
                      | statement_list"""
    pass


def p_statement(p: P):
    """statement : PRINT_SHEET SHEET_IDENT"""
    statement_name = None
    # TODO: Verify "statement name" from the staff.
    #if p[1] == 'print_sheet':
    #     statement_name = 'statement'
    print(f"statement({p[1]})")


def p_cell_ref(p: P):
    """cell_ref : SHEET_IDENT SQUOTE COORDINATE_IDENT
                | DOLLAR COLON RANGE_IDENT
                | DOLLAR
    """
    print(p[1])


def p_atom(p: P):
    """atom : IDENT
            | DECIMAL_LITERAL
            | cell_ref
    """
    print("atom", p[0])


def p_error(p: P):
    print(f"{p.lineno}:Syntax Error (token:'{p.value}')")
    raise SystemExit


parser: ply.yacc.LRParser = ply.yacc.yacc()


def parse_data(data: str):
    parser.parse(data, lexer=sslexer.lexer, debug=False)

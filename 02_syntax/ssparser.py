from ply import yacc

import sslexer

parser: yacc.LRParser = yacc.yacc()


def parse_data(data: str):
    parser.parse(data, lexer=sslexer.lexer, debug=False)

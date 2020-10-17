from unittest import TestCase

import ssparser


class SSParserTest(TestCase):
    """
    It seems like it is is too hard to test individual definition.
    So only test the top level ones.
    """

    def test_scalar_definition(self):
        # SCALAR IDENT
        ssparser.parse_data(data="scalar testy")

        # SCALAR IDENT EQ scalar_expr
        ssparser.parse_data(data="scalar testyScal = 3.0")


    def test_range_definition(self):
        # RANGE RANGE_IDENT
        ssparser.parse_data(data="range _rango2")

        # RANGE RANGE_IDENT EQ range_xpr
        ssparser.parse_data(data="range _rango = _rident")


    def test_sheet_definition(self):
        # SHEET SHEET_IDENT
        ssparser.parse_data(data="sheet SH")

        # SHEET SHEET_IDENT sheet_init
        # SHEET SHEET_IDENT sheet_init EQ sheet_init_list
        # SHEET SHEET_IDENT sheet_init EQ LRCURLY sheet_row RCURLY
        # SHEET SHEET_IDENT sheet_init EQ LRCURLY simple_expr RCURLY
        ssparser.parse_data(data="sheet SHINTROW = {3.0 * 5.0}")

        # SHEET SHEET_IDENT sheet_init EQ LRCURLY simple_expr {COMMA simple_expr} RCURLY

        # SHEET SHEET_IDENT sheet_init EQ INT_LITERAL MULT INT_LITERAL
        ssparser.parse_data(data="sheet SHINTMULT = 2 * 4")


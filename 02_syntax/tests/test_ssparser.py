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
        # Sheet definition
        pass

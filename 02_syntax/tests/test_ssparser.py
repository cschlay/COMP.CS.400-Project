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


    def test_range_definition(self):
        # Range definition
        pass

    def test_sheet_definition(self):
        # Sheet definition
        pass

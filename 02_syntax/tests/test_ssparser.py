from unittest import TestCase

import ssparser


class SSParserTest(TestCase):
    def test_statement(self):
        # PRINT_SHEET SHEET_IDENT
        ssparser.parse_data(data='print_sheet A')
        # PRINT_SHEET [INFO_STRING] SHEET_IDENT
        ssparser.parse_data(data='print_sheet !batman! BAT')

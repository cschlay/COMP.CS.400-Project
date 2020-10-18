from unittest import TestCase

import ssparser


class SSParserTest(TestCase):
    """
    It seems like it is is too hard to test individual definition.
    So I only attempt to write a valid SheetScript code.
    """

    def test_program(self):
        program = """
        scalar scal1 = 1.0
        scalar scal2 = scal1
        """
        ssparser.parse_data(data=program)

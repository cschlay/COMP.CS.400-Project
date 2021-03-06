from unittest import TestCase

import ssparser


class SSParserTest(TestCase):
    """
    It seems like it is is too hard to test individual definition.
    So I only attempt to write a valid SheetScript code.
    """

    def test_program(self):
        program = """
        ... Some variable declarations ...
        scalar scal1 = 1.0
        scalar scal2 = scal1 + 1.0 * 2.0 + 1.0
        
        ... ...
        ... Statement list ...
        ... ...
        
        ... prints ...
        print_sheet SH
        print_sheet !THIS IS SHEET! SH
        
        ... assignments ...
        ident1 := 1.0
        """
        ssparser.parse_data(data=program)

import unittest

from main import tokenize_file


class TokenizationBasicTest(unittest.TestCase):
    @staticmethod
    def test_tokenize_file():
        # This should just print, the purpose is to ensure that console displays properly.
        tokenize_file(filename="tests/code.sheetscript")

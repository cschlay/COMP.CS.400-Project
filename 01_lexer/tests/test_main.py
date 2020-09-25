import unittest

from main import tokenize_file


class TokenizationTest(unittest.TestCase):
    @staticmethod
    def test_tokenize_file():
        tokenize_file(filename="code.sheetscript")

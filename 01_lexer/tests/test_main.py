import unittest

import sslexer
from main import tokenize_file


class TokenizationBasicTest(unittest.TestCase):
    @staticmethod
    def test_tokenize_file():
        tokenize_file(filename="code.sheetscript")

    @staticmethod
    def test_tokenize_data():
        sslexer.tokenize_data(data="INVALID TOKEN")

from unittest import TestCase

import sslexer


class TokenDistinguishTest(TestCase):
    def test_function_and_variable_name(self):
        tokens = sslexer.tokenize_data(data="Function variable")
        self.assertEqual(tokens[0].type, "FUNC_IDENT")
        self.assertEqual(tokens[1].type, "IDENT")

    def test_keyword_and_variable_name(self):
        tokens = sslexer.tokenize_data(data="if ifs")
        self.assertEqual(tokens[0].type, "IF")
        self.assertEqual(tokens[1].type, "IDENT")

    def test_operator_gt_and_gte(self):
        pass

    def test_operator_lt_and_lte(self):
        pass

    def test_string_literals_and_variable_name(self):
        pass

    def test_comment_and_other_code(self):
        pass

    def test_integer_literals_and_decimal_literals(self):
        pass


"""
Unit-tests for preprocessing module
"""

import unittest

from core.translator.preprocessing import minify_text


class TestPreprocessing(unittest.TestCase):
    """
    TestCase for checking preprocessing correctness
    """

    def test_remove_comments(self):
        """
        Test removing assembly comments in text
        """
        code: str = (
            '; Hello this is assembly code\n'
            'xor rax, rax ; Clear rax\n'
            '; Another comment;'
        )
        expected: str = (
            'xor rax, rax'
        )
        output: str = minify_text(code)
        self.assertEqual(output, expected)

    def test_remove_extra_spaces(self):
        """
        Test removing extra spaces and tabs in text
        """
        code: str = (
            'xor            rax,  rax\n'
            '       xor rax,\trax'
        )
        expected: str = (
            'xor rax, rax\n'
            'xor rax, rax'
        )
        output: str = minify_text(code)
        self.assertEqual(output, expected)

    def test_remove_empty_lines(self):
        """
        Test removing empty lines in text
        """
        code: str = (
            '; hello\n'
            ';\n'
            'xor            rax,  rax\n'
            '\n     '
        )
        expected: str = (
            'xor rax, rax'
        )
        output: str = minify_text(code)
        self.assertEqual(output, expected)

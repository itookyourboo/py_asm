"""
Integration tests for py-asm execution correctness
"""

import sys

from unittest import TestCase
from subprocess import check_output


class TestCatProgram(TestCase):
    """
    Test cat.pyasm program
        - Input: word X
        - Output: word X
    """

    def test_input(self) -> None:
        """
        Run program and check input and output for equality
        """
        filename: str = './test/examples/cat.pyasm'
        command: list[str] = [sys.executable, 'main.py', 'run', filename]

        messages: list[str] = [
            'hello',
            'hello world',
            '12345',
            'cat',
            'first_line\nsecond_line',
            'this\n\tis\n\t\tsparta'
        ]
        for message in messages:
            with self.subTest(message=message):
                result: str = check_output(
                    command,
                    input=message.encode()
                ).decode()
                self.assertEqual(message, result)

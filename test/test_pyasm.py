"""
Integration tests for py-asm execution correctness
"""

import sys

from unittest import TestCase
from subprocess import check_output


class TestHelloProgram(TestCase):
    """
    Test hello.pyasm program
        - Output: Hello world
    """

    def test_input(self) -> None:
        """
        Run program and check if output equals "hello world"
        """
        filename: str = './test/examples/hello.pyasm'
        command: list[str] = [sys.executable, 'main.py', 'run', filename]
        expected: str = 'hello world'

        result: str = check_output(command).decode()
        self.assertEqual(expected, result)


class TestCatProgram(TestCase):
    """
    Test cat.pyasm program
        - Input: word X
        - Output: word X
    """

    def test_output(self) -> None:
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


class TestProb5Program(TestCase):
    """
    Test prob5.pyasm program

    2520 is the smallest number that can be divided by each of the numbers
    from 1 to 10 without any remainder. What is the smallest positive number
    that is evenly divisible by all the numbers from 1 to 20?
    """

    def test_answer(self) -> None:
        """
        Run program and check if answer is correct
        """
        filename: str = './test/examples/prob5.pyasm'
        command: list[str] = [sys.executable, 'main.py', 'run', filename]

        cases: dict[int, int] = {
            5: 60,
            7: 420,
            10: 2520,
            20: 232792560,
            21: 232792560
        }
        for num, expected in cases.items():
            with self.subTest(N=num):
                result: str = check_output(
                    command,
                    input=str(num).encode()
                ).decode()
                answer: int = int(result)
                self.assertEqual(expected, answer)

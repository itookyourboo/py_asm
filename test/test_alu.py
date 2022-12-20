"""
Unit-tests for ALU
"""

import unittest

from core.machine.config import MAX_NUM, MIN_NUM

from core.machine.alu import (
    _get_sign,
    _get_zero,
    _get_carry,
    _get_overflow
)


class TestALU(unittest.TestCase):
    """
    TestCase for checking preprocessing correctness
    """

    def test_zero_flag(self):
        """
        Test zero checking correctness
        """
        cases: dict[int, int] = {
            0: True,
            1: False,
            MAX_NUM: False,
            MAX_NUM // 2: False,
            MAX_NUM + 1: False,
            MIN_NUM: False,
            MIN_NUM // 2: False,
            MIN_NUM - 1: False
        }

        for num, expected in cases.items():
            with self.subTest(num=num):
                self.assertEqual(_get_zero(num), expected)

    def test_sign_flag(self):
        """
        Test sign checking correctness
        """
        cases: dict[int, int] = {
            0: False,
            1: False,
            -1: True,
            MAX_NUM: False,
            MIN_NUM: True,
            MIN_NUM - 1: False,
            MAX_NUM + 1: True
        }

        for num, expected in cases.items():
            with self.subTest(num=num):
                self.assertEqual(_get_sign(num), expected)

    def test_overflow_flag(self):
        """
        Test overflow checking correctness
        """
        cases: dict[int, int] = {
            0: False,
            1: False,
            -1: False,
            MAX_NUM: False,
            MIN_NUM: False,
            MIN_NUM - 1: True,
            MAX_NUM + 1: True
        }

        for num, expected in cases.items():
            with self.subTest(num=num):
                self.assertEqual(_get_overflow(num), expected)

    def test_carry_flag(self):
        """
        Test carry checking correctness
        """
        cases: dict[int, int] = {
            0: False,
            1: False,
            -1: False,
            MIN_NUM: False,
            MAX_NUM: False,
            2 * MAX_NUM + 2: True,
            2 * MIN_NUM - 2: True
        }

        for num, expected in cases.items():
            with self.subTest(num=num):
                self.assertEqual(_get_carry(num), expected)

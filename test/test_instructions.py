"""
Unit-tests for Instruction Controller
"""

import unittest

from core.exceptions import RegisterIsNotWritable, OperandIsNotWriteable
from core.machine import Computer
from core.machine.instruction_controller import InstructionController
from core.model import Instruction, Operand, Register, Constant, Address


class TestInstruction(unittest.TestCase):
    """
    TestCase for checking instruction execution correctness
    """
    def setUp(self) -> None:
        """
        Set up computer with 4 memory data cells
        """

        self.computer: Computer = Computer()
        self.computer.m_controller.load_data([0, 0, 0, 0])
        self.executor: InstructionController = (
            self.computer.instruction_executor
        )

    def test_destination_set(self):
        """
        Test set_operand_value method
        """
        value: int = 0xDEAD
        destinations: list[Operand] = [
            Register('RAX'),
            Register('RDX'),
            Address(1),
            Address(2)
        ]
        for dest in destinations:
            [*_] = self.executor.execute(
                Instruction(
                    name='mov',
                    operands=[dest, Constant(value)]
                )
            )
            self.assertEqual(self.executor.get_operand_value(dest), value)

    def test_unable_to_set_rip_value(self):
        """
        Try to set RIP value. Error should be raised
        """
        with self.assertRaises(RegisterIsNotWritable):
            [*_] = self.executor.execute(
                Instruction(
                    name='mov',
                    operands=[Register('RIP'), Constant(1)]
                )
            )

    def test_unable_to_write_into_constant(self):
        """
        Try to set Constant operand value. Error should be raised.
        """
        with self.assertRaises(OperandIsNotWriteable):
            [*_] = self.executor.execute(
                Instruction(
                    name='mov',
                    operands=[Constant(0), Constant(1)]
                )
            )

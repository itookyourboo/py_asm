"""
Unit-tests for translator module
"""
import pickle
from unittest import TestCase

from core.exceptions import UnexpectedOperand
from core.model import (
    Program, DataSection, TextSection, Instruction, Register,
    Constant, Address, IndirectAddress, Operand, Label
)
from core.translator.translator import parse_operand, parse_instruction


class TestTranslator(TestCase):
    """
    TestCase for checking preprocessing correctness
    """

    def test_correct_pickle(self):
        """
        Test serialization correctness
        """
        program: Program = Program(
            data=DataSection(
                var_to_addr={'X': 0},
                memory=[0, 0, 0]
            ),
            text=TextSection(
                labels={},
                lines=[
                    Instruction(
                        name='xor',
                        operands=[
                            Register('RAX'),
                            Constant(19),
                            Address(value=0),
                            IndirectAddress(
                                offset=Register('RDI'),
                                label='X'
                            )
                        ]
                    ),
                    Instruction(name='hlt')
                ]
            )
        )

        self.assertEqual(
            program,
            pickle.loads(
                pickle.dumps(program)
            )
        )

    def test_parse_operand(self):
        """
        Test parse operand correctness
        """
        cases: dict[str, Operand] = {
            '%rax': Register('RAX'),
            '7': Constant(7),
            '0xDEAD': Constant(0xDEAD),
            '#X': Address(label='X'),
            '.label': Label(name='.label'),
            '#X[0]': IndirectAddress(
                offset=Constant(0),
                label='X'
            )
        }
        for operand_str, expected in cases.items():
            with self.subTest(
                    operand_str=operand_str,
            ):
                self.assertEqual(
                    expected,
                    parse_operand(operand_str)
                )

    def test_parse_fake_operand(self):
        """
        Test parse unexpected operand correctness
        """
        fakes: list[str] = [
            '#4',
            '%MEOW',
            '-omg',
            '0xWTF'
        ]
        for fake in fakes:
            with (
                self.subTest(operand=fake),
                self.assertRaises(UnexpectedOperand),
            ):
                parse_operand(fake)

    def test_parse_instruction(self):
        """
        Test parse instruction correctness
        """
        cases: dict[str, Instruction] = {
            'ADD %rax, 5, #X': Instruction(
                name='add',
                operands=[
                    Register('RAX'),
                    Constant(5),
                    Address(label='X')
                ]
            ),
            'XOR %rax, %RBX': Instruction(
                name='xor',
                operands=[
                    Register('RAX'),
                    Register('RBX')
                ]
            ),
            'INC #X': Instruction(
                name='inc',
                operands=[
                    Address(label='X')
                ]
            ),
            'HLT': Instruction(
                name='hlt',
                operands=[]
            )
        }

        for instruction_str, expected in cases.items():
            with self.subTest(instruction=instruction_str):
                self.assertEqual(
                    expected,
                    parse_instruction(instruction_str)
                )

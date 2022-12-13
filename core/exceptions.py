"""
Custom exceptions
"""


class _Exception(Exception):
    """
    Base Exception class
    """
    pass


class UndefinedInstruction(_Exception):
    """
    Invoked when user writes some undefined instruction in code
    """
    pass


class UndefinedLOC(_Exception):
    """
    Invoked when translator can't classify line as Label or Instruction
    """
    pass


class UnexpectedOperand(_Exception):
    """
    Invoked when translator couldn't parse operand
    """
    pass


class UnexpectedArguments(_Exception):
    """
    Invoked when instruction argument type doesn't match expected
    """
    pass


class UnexpectedDataValue(_Exception):
    """
    Invoked when data value is neither number nor string
    """
    pass


class TextSectionNotFound(_Exception):
    """
    Invoked when
        section .text
    in assembly code not found
    """
    pass

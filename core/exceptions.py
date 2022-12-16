"""
Custom exceptions
"""


class PyAsmException(Exception):
    """
    Base Exception class
    """
    pass


class UndefinedInstruction(PyAsmException):
    """
    Raised when there is no such instruction
    """
    pass


class UndefinedLOC(PyAsmException):
    """
    Raised when translator can't classify line as Label or Instruction
    """
    pass


class UnexpectedOperand(PyAsmException):
    """
    Raised when translator couldn't parse operand
    """
    pass


class UnexpectedArguments(PyAsmException):
    """
    Raised when instruction argument type doesn't match expected
    """
    pass


class NotEnoughOperands(PyAsmException):
    """
    Raised when instruction needs more operands
    """
    pass


class UnexpectedDataValue(PyAsmException):
    """
    Raised when data value is neither number nor string
    """
    pass


class TextSectionNotFound(PyAsmException):
    """
    Raised when
        section .text
    in assembly code not found
    """
    pass


class DataNotFound(PyAsmException):
    """
    Raised when variable in data section not found
    """
    pass


class IncorrectDataType(PyAsmException):
    """
    Raised when needed data has another type
    """
    pass


class ConstantIsNotWriteable(PyAsmException):
    """
    Raised when trying to write in constant
    """
    pass


class NoSuchLabel(PyAsmException):
    """
    Raised when translator can not find label
    """
    pass


class ProgramExit(PyAsmException):
    """
    End of program
    """
    pass


class NumberOutOfRange(PyAsmException):
    """
    Raised when number in code is out of range
    """
    pass

from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass, field
from types import UnionType
from typing import Type, Callable


class Serializable(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def from_dict(self, data: dict) -> 'Serializable':
        raise NotImplementedError


class Operand(Serializable, ABC):
    pass


@dataclass
class Constant(Operand, ABC):
    value: str | int


@dataclass
class String(Constant):
    value: str

    def to_dict(self) -> dict:
        return {
            self.__class__.__name__: self.value
        }

    def from_dict(self, data: dict) -> 'String':
        return self


@dataclass
class Number(Constant):
    value: int

    def to_dict(self) -> dict:
        return {
            self.__class__.__name__: self.value
        }

    def from_dict(self, data: dict) -> 'Number':
        return self


@dataclass
class RegisterInfo(Serializable):
    can_read: bool
    can_write: bool
    size: int

    value: int = 0

    def to_dict(self) -> dict:
        return {
            self.__class__.__name__: {
                'can_read': self.can_read,
                'can_write': self.can_write,
                'size': self.size
            }
        }

    def from_dict(self, data: dict) -> 'RegisterInfo':
        return self


def _register_data():
    return RegisterInfo(
        can_read=True,
        can_write=True,
        size=4
    )


def _register_pointer():
    return RegisterInfo(
        can_read=True,
        can_write=False,
        size=4
    )


def _register_index():
    return RegisterInfo(
        can_read=True,
        can_write=True,
        size=4
    )


def _register_control():
    return RegisterInfo(
        can_read=True,
        can_write=False,
        size=1
    )


@dataclass
class Expression:
    operations: list[Callable]
    operands: list[Operand]


class MetaSerializable(metaclass=type(Serializable)):
    pass


class MetaEnum(metaclass=type(Enum)):
    pass


class OperandEnum(type(MetaSerializable), type(MetaEnum)):
    pass


class Register(Operand, Serializable, Enum, metaclass=OperandEnum):
    RAX = _register_data()
    RBX = _register_data()
    RCX = _register_data()
    RDX = _register_data()

    RIP = _register_pointer()
    RSP = _register_pointer()
    RBP = _register_pointer()

    RSI = _register_index()
    RDI = _register_index()

    RFL = _register_control()

    def to_dict(self) -> dict:
        return {
            self.__class__.__name__: {
                'name': self.name,
                'info': self.value.to_dict()
            }
        }

    def from_dict(self, data: dict) -> 'Register':
        return self


@dataclass
class Address(Operand, ABC):
    pass


@dataclass
class DirectAddress(Address):
    def to_dict(self) -> dict:
        return {
            self.__class__.__name__: {
            }
        }

    def from_dict(self, data: dict) -> 'DirectAddress':
        return self


@dataclass
class IndirectAddress(Address):
    def to_dict(self) -> dict:
        return {
            self.__class__.__name__: {
            }
        }

    def from_dict(self, data: dict) -> 'IndirectAddress':
        return self


class LOC(Serializable, ABC):
    pass


@dataclass
class Label(LOC, Operand):
    name: str

    def to_dict(self) -> dict:
        return {
            self.__class__.__name__: {
                'name': self.name
            }
        }

    def from_dict(self, data: dict) -> 'Label':
        return self


@dataclass
class InstructionInfo(Serializable):
    operand_types: set[tuple[UnionType | Type[Operand], ...]]
    operand_values: list[Operand] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            self.__class__.__name__: {
                'operands': [
                    operand.to_dict() for operand in self.operand_values
                ]
            }
        }

    def from_dict(self, data: dict) -> 'InstructionInfo':
        return self


class MetaLOC(metaclass=type(LOC)):
    pass


class LOCEnum(type(MetaLOC), type(MetaEnum)):
    pass


@dataclass
class Instruction(LOC, Enum, metaclass=LOCEnum):
    XOR = InstructionInfo(operand_types={
        (Address | Register, Address | Register | Constant)
    })
    ADD = InstructionInfo(operand_types={
        (Address | Register, Address | Register | Number)
    })
    AND = InstructionInfo(operand_types={
        (Address | Register, Address | Register | Number)
    })
    CALL = InstructionInfo(operand_types={
        (Label,)
    })
    CMP = InstructionInfo(operand_types={
        (Address | Register, Address | Register | Constant)
    })
    DEC = InstructionInfo(operand_types={
        (Address | Register,)
    })
    DIV = InstructionInfo(operand_types={
        (Address | Register, Address | Register | Number)
    })
    INC = InstructionInfo(operand_types={
        (Address | Register,)
    })
    RET = InstructionInfo(operand_types={
        (Address | Register, Address | Register | Constant)
    })

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'name={self.name!r}, '
            f'value={self.value!r}'
            f')'
        )

    def __str__(self):
        return self.__repr__()

    def to_dict(self) -> dict:
        return {
            self.__class__.__name__: {
                'name': self.name,
                'info': self.value.to_dict()
            }
        }

    def from_dict(self, data: dict) -> 'Instruction':
        return self

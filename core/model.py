from dataclasses import dataclass, field
from types import UnionType
from typing import Type, Callable


class Operand:
    pass


@dataclass
class Constant(Operand):
    value: str | int


@dataclass
class String(Constant):
    value: str


@dataclass
class Number(Constant):
    value: int


@dataclass
class RegisterInfo:
    can_read: bool
    can_write: bool
    size: int

    value: int = 0


@dataclass
class Expression:
    operations: list[Callable]
    operands: list[Operand]


@dataclass
class Register(Operand):
    name: str
    info: RegisterInfo


@dataclass
class Address(Operand):
    value: int


class LOC:
    pass


@dataclass
class Label(LOC, Operand):
    name: str


@dataclass
class InstructionInfo:
    operand_types: set[tuple[UnionType | Type[Operand], ...]]
    operand_values: list[Operand] = field(default_factory=list)


@dataclass
class Instruction(LOC):
    name: str
    info: InstructionInfo


@dataclass
class DataSection:
    data: dict[str, Constant] = field(default_factory=dict)


@dataclass
class TextSection:
    labels: dict[str, int] = field(default_factory=dict)
    lines: list[LOC] = field(default_factory=list)


@dataclass
class Program:
    data: DataSection = field(default_factory=DataSection)
    text: TextSection = field(default_factory=TextSection)

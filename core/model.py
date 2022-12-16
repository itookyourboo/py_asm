from dataclasses import dataclass, field
from typing import TypeAlias


class Operand:
    value: str | int

    def __str__(self) -> str:
        return str(self.value)


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


@dataclass
class Register(Operand):
    value: str


@dataclass
class Address(Operand):
    value: str


class LOC:
    pass


@dataclass
class Label(LOC, Operand):
    value: str
    index: int = -1


@dataclass
class Instruction(LOC):
    name: str
    operands: list[Operand] = field(default_factory=list)

    def __str__(self) -> str:
        op_str: str = ', '.join(map(str, self.operands))
        return f'{self.name} {op_str}'


@dataclass
class DataSection:
    data: dict[str, Constant] = field(default_factory=dict)


@dataclass
class TextSection:
    labels: dict[str, int] = field(default_factory=dict)
    lines: list[Instruction] = field(default_factory=list)


@dataclass
class Program:
    data: DataSection = field(default_factory=DataSection)
    text: TextSection = field(default_factory=TextSection)


Destination: TypeAlias = Address | Register
Source: TypeAlias = Address | Register | Constant

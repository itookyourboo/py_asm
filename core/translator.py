# pylint: disable=import-error
# mypy: ignore_missing_imports=True

"""
Translating .asm code into object file
"""
from types import UnionType
from typing import Iterator, Type

from core.exceptions import (
    UndefinedInstruction, UndefinedLOC, UnexpectedOperand, UnexpectedArguments
)
from core.model import (
    Instruction, LOC, Label, Operand, Register, Number, String
)
from core.util import (
    is_number, is_string, is_register, is_label, convert_to_number
)
from preprocessing import minify_text
from json import dumps


def parse_operand(operand_str: str) -> Operand:
    if is_number(operand_str):
        return Number(value=convert_to_number(operand_str))
    if is_string(operand_str):
        return String(value=operand_str[1:-1])
    if is_register(operand_str):
        return Register[operand_str.upper()]
    # if is_expression(operand_str):
    #     return Expression()
    if is_label(operand_str):
        return Label(name=operand_str)

    raise UnexpectedOperand


def parse_operands(line: str) -> list[Operand]:
    if ',' not in line:
        pass

    operands_str = map(str.strip, line.split(','))
    operands = map(parse_operand, operands_str)

    return list(operands)


def fill_operand_values(
        instruction: Instruction,
        operands: list[Operand]
) -> None:
    inst_types: tuple[UnionType | Type, ...]
    for inst_types in instruction.value.operand_types:
        if len(operands) != len(inst_types):
            continue

        if all(
                isinstance(op, inst_type)
                for op, inst_type in zip(operands, inst_types)
        ):
            instruction.value.operand_values.extend(operands)
            break
    else:
        op_types: list[Type] = list(map(type, operands))
        expected: list[tuple[Type, ...]] = list(
            instruction.value.operand_types.keys()
        )
        raise UnexpectedArguments(
            f'Given: {op_types!r}\n'
            f'Expected: {expected!r}'
        )


def parse_instruction(line: str) -> Instruction:
    cmd: str
    operands_str: str

    cmd, operands_str = line.split(' ', 1)
    cmd = cmd.upper()
    if cmd not in Instruction.__members__:
        raise UndefinedInstruction(cmd)

    instruction: Instruction = Instruction[cmd]
    operands: list[Operand] = parse_operands(operands_str)
    fill_operand_values(instruction, operands)

    return instruction


def parse_line(line: str) -> Iterator[LOC]:
    label: str = ''
    instruction_str: str = line

    if ':' in line:
        label, instruction_str = map(str.strip, line.split(':', 1))

    if not is_label(label) and not instruction_str:
        raise UndefinedLOC(line)

    if is_label(label):
        yield Label(label)

    if instruction_str:
        yield parse_instruction(instruction_str)


def translate_line(line: str) -> Iterator[dict]:
    yield from [obj.to_dict() for obj in parse_line(line)]


def translate(code: str) -> dict:
    result: dict = {
        'lines': []
    }

    line: str
    for line in code.splitlines():
        loc_dict: dict
        for loc_dict in translate_line(line):
            result['lines'].append(loc_dict)

    return result


if __name__ == '__main__':
    with (
        open('../examples/program.asm', encoding='utf8') as file,
        open('../examples/program.asm.o', 'w', encoding='utf8') as output
    ):
        source_code: str = file.read()
        minified: str = minify_text(source_code)
        translated: dict = translate(minified)
        output.write(dumps(translated, ensure_ascii=False, indent=4))

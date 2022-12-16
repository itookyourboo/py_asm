# pylint: disable=import-error
# mypy: ignore_missing_imports=True

"""
Translating .asm code into object file
"""
import pickle
import re
import warnings
from typing import Iterator

from core.config import MIN_NUM, MAX_NUM, NULL_TERM
from core.exceptions import (
    UndefinedInstruction, UndefinedLOC, UnexpectedOperand,
    UnexpectedDataValue, TextSectionNotFound, NoSuchLabel, NumberOutOfRange
)
from core.machine.instructions import InstructionSet
from core.model import (
    Instruction, LOC, Label, Operand, Number,
    String, Program, Address, DataSection, Constant, TextSection, Register, IndirectAddress
)
from core.translator.util import (
    is_number, is_string, is_register, is_label, convert_to_number, is_address,
    is_direct_address, is_indirect_address
)
from core.translator.preprocessing import minify_text


def parse_operand(operand_str: str) -> Operand:
    if is_number(operand_str):
        return Number(value=convert_to_number(operand_str))
    if is_string(operand_str):
        operand_str = operand_str[1:-1]
        return String(value=operand_str)
    if is_register(operand_str):
        return Register(operand_str.upper()[1:])
    if is_indirect_address(operand_str):
        base, offset = operand_str.split('[')
        base = base[1:]
        offset = offset[:-1]
        return IndirectAddress(
            value=base,
            offset=parse_operand(offset)
        )
    if is_direct_address(operand_str):
        return Address(value=operand_str[1:])
    if is_label(operand_str):
        return Label(value=operand_str)

    raise UnexpectedOperand(f'"{operand_str}"')


def parse_operands(line: str) -> list[Operand]:
    if not line:
        return []

    if ',' not in line:
        pass

    operands_str = map(str.strip, line.split(','))
    operands = map(parse_operand, operands_str)

    return list(operands)


def fill_operand_values(
        instruction: Instruction,
        operands: list[Operand]
) -> None:
    instruction.operands.extend(operands)


def parse_instruction(line: str) -> Instruction:
    cmd: str
    operands_str: str = ''

    if ' ' not in line:
        cmd = line
    else:
        cmd, operands_str = line.split(' ', 1)

    cmd = cmd.lower()
    if cmd not in InstructionSet.get_all():
        err_template: str = '-->{}<--'
        raise UndefinedInstruction(
            line.replace(cmd, err_template.format(cmd))
            .replace(cmd.upper(), err_template.format(cmd.upper()))
        )

    instruction: Instruction = Instruction(cmd)
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


def parse_data_line(line: str) -> tuple[str, Constant]:
    key, value = map(str.strip, line.split(':', 1))

    if value.startswith('buf '):
        _, count = value.split(None, 1)
        buffer = chr(NULL_TERM) * int(count)
        return key, String(value=buffer)

    constant: Constant
    if is_number(value):
        constant = Number(value=convert_to_number(value))
    elif is_string(value):
        value = value[1:-1]
        value = value.replace('\\n', '\n')
        constant = String(value=value)
    else:
        raise UnexpectedDataValue

    return key, constant


def linearize_const(const: Constant) -> Iterator[int]:
    if isinstance(const, Number):
        if not (MIN_NUM <= const.value <= MAX_NUM):
            raise NumberOutOfRange(
                f'Number should be in range [{MIN_NUM}; {MAX_NUM}]'
            )
        yield const.value
    else:
        yield from map(ord, const.value.replace('\\\\', '\\'))
        yield NULL_TERM


def parse_data_section(code: str) -> DataSection:
    data: dict[str, int] = {}
    memory: list[int] = []

    for line in code.splitlines():
        key, constant = parse_data_line(line)
        if key in data:
            warnings.warn(f'Redefinition of variable "{key}": '
                          f'{data[key]} -> {constant}')
        data[key] = len(memory)
        memory.extend(linearize_const(constant))

    return DataSection(
        var_to_addr=data,
        memory=memory
    )


def set_labels_indexes(
        lines: list[Instruction],
        labels: dict[str, int]
) -> None:
    i: int
    inst: Instruction
    for i, inst in enumerate(lines):
        operand: Operand
        for operand in inst.operands:
            if not isinstance(operand, Label):
                continue
            if operand.value not in labels:
                raise NoSuchLabel
            operand.index = labels[operand.value]


def parse_text_section(code: str) -> TextSection:
    labels: dict[str, int] = {}
    lines: list[Instruction] = []

    line: str
    for line in code.splitlines():
        loc: LOC
        for loc in parse_line(line):
            if isinstance(loc, Label):
                if loc.value in labels:
                    warnings.warn(f'Redefinition of label "{loc.value}"')

                labels[loc.value] = len(lines)
            elif isinstance(loc, Instruction):
                lines.append(loc)
            else:
                raise TypeError(
                    f'Incorrect LOC type: {type(loc)}. '
                    f'Expected {LOC.__subclasses__()}'
                )

    set_labels_indexes(lines, labels)

    return TextSection(
        labels=labels,
        lines=lines
    )


def set_addresses_indexes(
        lines: list[Instruction],
        var_to_addr: dict[str, int]
) -> None:
    inst: Instruction
    for inst in lines:
        op: Operand
        for op in inst.operands:
            if isinstance(op, (Address, IndirectAddress)):
                op.index = var_to_addr[op.value]


_SECTION_TEXT = 'section .text'
_SECTION_DATA = 'section .data'


def parse_code(code: str) -> Program:
    text_index: int = code.find(_SECTION_TEXT)
    if text_index == -1:
        raise TextSectionNotFound

    text_start, text_stop = text_index + len(_SECTION_TEXT) + 1, None

    data_index: int = code.find(_SECTION_DATA)
    if data_index == -1:
        return Program(
            text=parse_text_section(code[text_start:text_stop])
        )

    data_start, data_stop = data_index + len(_SECTION_DATA) + 1, None

    if text_index < data_index:
        text_stop = data_index - 1
    else:
        data_stop = text_index - 1

    program: Program = Program(
        data=parse_data_section(code[data_start:data_stop]),
        text=parse_text_section(code[text_start:text_stop])
    )

    set_addresses_indexes(program.text.lines, program.data.var_to_addr)

    return program


if __name__ == '__main__':
    from pprint import pprint

    filename = 'cat'

    source = f'../examples/{filename}.pyasm'
    dest = f'../examples/{filename}.pyasm.o'

    # translating
    with open(source) as file:
        source_code: str = file.read()
        minified: str = minify_text(source_code)
        program: Program = parse_code(minified)

    # dumping
    with open(dest, 'wb') as output:
        pickle.dump(program, output)

    # reading
    with open(dest, 'rb') as object_file:
        prog: Program = pickle.load(object_file)
        pprint(prog)

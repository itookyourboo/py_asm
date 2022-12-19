"""
CLI interface to translate and execute assembler
"""
import warnings
import sys
from typing import Optional, Type

import typer

from core.exceptions import PyAsmException
from core.file_helper import translate_asm_file, read_program_from_file
from core.model import Program
from core.machine import Computer

app = typer.Typer(help='Assembler translator')


def print_exception(error: PyAsmException) -> None:
    """
    Print PyAsmException message in stderr
    """
    exc_type: Type[PyAsmException] = type(error)
    typer.echo(
        typer.style(
            f'{exc_type.__name__}: {error!s}',
            fg=typer.colors.RED
        ) +
        typer.style(
            f'{exc_type.__doc__}',
            fg=typer.colors.BRIGHT_RED
        ), err=True
    )


@app.command(name="translate")
def translate(
        asm_file_name: str,
        object_file_name: Optional[str] = None,
        verbose: Optional[bool] = False
) -> None:
    """
    Translate .asm code to object file
    """
    if object_file_name is None:
        object_file_name = f'{asm_file_name}.o'

    warnings.filterwarnings(
        "default" if verbose else "ignore"
    )

    try:
        translate_asm_file(asm_file_name, object_file_name)
    except PyAsmException as error:
        print_exception(error)
        sys.exit(1)


@app.command(name="exec")
def execute(
        obj_file_name: str,
        trace: Optional[bool] = False
) -> None:
    """
    Execute object file
    """

    program: Program = read_program_from_file(obj_file_name)
    computer: Computer = Computer()
    try:
        for ex in computer.execute_program(program):
            if not trace:
                continue
            print(str(ex.instruction_executor.current))
            print('Registers:', ex.r_controller)
            print('ALU', ex.alu)
            print('Memory:', ex.m_controller)
            print('Clock:', ex.clock)
    except PyAsmException as error:
        print_exception(error)
        sys.exit(1)


@app.command(name="run")
def run(
        asm_file_name: str,
        object_file_name: Optional[str] = None,
        verbose: Optional[bool] = False,
        trace: Optional[bool] = False
) -> None:
    """
    Translate and execute .pyasm file
    """

    if object_file_name is None:
        object_file_name = f'{asm_file_name}.o'

    try:
        translate(asm_file_name, object_file_name, verbose)
        execute(object_file_name, trace)
    except PyAsmException as error:
        print_exception(error)
        sys.exit(1)


if __name__ == '__main__':
    app()

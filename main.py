"""
CLI interface to translate and execute assembler
"""
import warnings
from typing import Optional
from pprint import pprint

import typer

from core.io import translate_asm_file, read_program_from_file
from core.model import Program

app = typer.Typer(help='Assembler translator')


@app.command(name="translate")
def translate_cmd(
        asm_file_name: str,
        object_file_name: Optional[str] = None,
        verbose: Optional[bool] = False
):
    """
    Translate .asm code to object file
    """
    if object_file_name is None:
        object_file_name = f'{asm_file_name}.o'

    warnings.filterwarnings(
        "default" if verbose else "ignore"
    )

    translate_asm_file(asm_file_name, object_file_name)


@app.command(name="exec")
def execute(obj_file_name: str):
    """
    Execute object file
    """
    typer.echo(f'Executing {obj_file_name}...')

    program: Program = read_program_from_file(obj_file_name)
    pprint(program)


if __name__ == '__main__':
    app()

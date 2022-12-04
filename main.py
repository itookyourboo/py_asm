"""
CLI interface to translate and execute assembler
"""

import typer

app = typer.Typer(help='Assembler translator')


@app.command()
def translate(
        asm_file: typer.FileText,
        verbose: bool = False
):
    """
    Translate .asm code to object file
    """
    typer.echo(f'Translating {asm_file}...')
    if verbose:
        typer.echo('- Some verbose operation')


@app.command(name="exec")
def execute(obj_file: typer.FileText):
    """
    Execute object file
    """
    typer.echo(f'Executing {obj_file}...')


if __name__ == '__main__':
    app()

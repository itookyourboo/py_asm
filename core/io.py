import pickle

from core.model import Program
from core.preprocessing import minify_text
from core.translator import parse_code


def translate_asm_file(asm_file_name: str, object_file_name: str) -> None:
    source_code: str = read_source_code(asm_file_name)
    minified_code: str = minify_text(source_code)
    program: Program = parse_code(minified_code)
    write_program_to_file(program, object_file_name)


def read_source_code(file_name: str) -> str:
    with open(file_name, 'r') as asm_file:
        return asm_file.read()


def read_program_from_file(file_name: str) -> Program:
    with open(file_name, 'rb') as object_file:
        return pickle.load(object_file)


def write_program_to_file(program: Program, file_name: str) -> None:
    with open(file_name, 'wb') as object_file:
        pickle.dump(program, object_file, protocol=pickle.HIGHEST_PROTOCOL)

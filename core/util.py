"""
Util-functions for working with data
"""

import re

from core.model import Register

RE_NEG = r'-?'
RE_HEX = r'0[xX][0-9a-fA-F]+'
RE_OCT = r'0[oO][0-7]+'
RE_BIN = r'0[bB][01]+'
RE_DEC = r'[0-9]+'
RE_NUM = rf'{RE_NEG}({RE_DEC}|{RE_BIN}|{RE_OCT}|{RE_HEX})'

RE_REG = r'|'.join(map(lambda reg: f'({reg})', Register.__members__.keys()))

RE_OPR = rf'({RE_NUM})|({RE_REG})'

RE_STR = r'^[\'\"].*[\'\"]$'
RE_EXP = rf'\[({RE_OPR})[\+\-]({RE_OPR})\]'

RE_LBL = r'\.?[a-zA-Z_]+'


def is_number(string: str) -> bool:
    return bool(
        re.fullmatch(
            RE_NUM,
            string.upper()
        )
    )


def convert_to_number(string: str) -> int:
    string = string.upper()

    if re.match(rf'{RE_NEG}{RE_HEX}', string):
        return int(string, 16)
    if re.match(rf'{RE_NEG}{RE_OCT}', string):
        return int(string, 8)
    if re.match(rf'{RE_NEG}{RE_BIN}', string):
        return int(string, 2)
    if re.match(rf'{RE_NEG}{RE_DEC}', string):
        return int(string)

    return 0


def is_string(string: str) -> bool:
    return bool(
        re.fullmatch(
            RE_STR,
            string
        )
    )


def is_register(string: str) -> bool:
    return bool(
        re.fullmatch(
            RE_REG,
            string.upper()
        )
    )


def is_expression(string: str) -> bool:
    return bool(
        re.fullmatch(
            RE_EXP,
            string.upper()
        )
    )


def is_label(string: str) -> bool:
    return bool(
        re.fullmatch(
            RE_LBL,
            string.upper()
        )
    )

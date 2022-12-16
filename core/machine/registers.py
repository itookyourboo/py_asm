from typing import Iterator

from core.machine.arithmetic import _strip_number
from core.model import RegisterInfo, Register


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


__available_registers__ = {
    'RAX': _register_data(),
    'RBX': _register_data(),
    'RCX': _register_data(),
    'RDX': _register_data(),
    'RSX': _register_data(),

    'RIP': _register_pointer(),
    'RSP': _register_pointer(),
    'RBP': _register_pointer(),

    'RSI': _register_index(),
    'RDI': _register_index(),

    'RFL': _register_control()
}


class RegisterController:
    def __init__(self):
        self.__states__: dict[str, int] = {
            register: 0 for register in self.keys()
        }

    def get(self, register: Register) -> int:
        return self.__states__[register.value]

    def set(self, register: Register, value: int | str) -> None:
        self.__states__[register.value] = _strip_number(value)

    def get_instruction_pointer(self) -> int:
        return self.__states__['RIP']

    def set_instruction_pointer(self, pointer: int) -> None:
        self.__states__['RIP'] = pointer

    def __repr__(self) -> str:
        return str(self.__states__)

    @staticmethod
    def contains(register_name: str) -> bool:
        return register_name in RegisterController.keys()

    @staticmethod
    def keys() -> Iterator[str]:
        yield from __available_registers__

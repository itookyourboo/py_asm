from typing import Iterator

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

    'RIP': _register_pointer(),
    'RSP': _register_pointer(),
    'RBP': _register_pointer(),

    'RSI': _register_index(),
    'RDI': _register_index(),

    'RFL': _register_control()
}


class RegisterController:
    __states__ = {
        register_name: Register(
            name=register_name,
            info=__available_registers__[register_name]
        ) for register_name in __available_registers__
    }

    @staticmethod
    def contains(register_name: str) -> bool:
        return register_name in __available_registers__

    @staticmethod
    def get_info(register_name: str) -> RegisterInfo:
        return __available_registers__[register_name]

    @classmethod
    def get(cls, register_name: str) -> Register:
        return cls.__states__[register_name]

    @staticmethod
    def keys() -> Iterator[str]:
        yield from __available_registers__

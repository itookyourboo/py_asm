from typing import Callable

from core.model import Register, Address, Label, Destination, Source


class InstructionSet:
    def i_add(self, dest: Destination, *ops: Source):
        raise NotImplementedError

    def i_sub(self, dest: Destination, *ops: Source):
        raise NotImplementedError

    def i_mul(self, dest: Destination, *ops: Source):
        raise NotImplementedError

    def i_div(self, dest: Destination, *ops: Source):
        raise NotImplementedError

    def i_xor(self, dest: Destination, *ops: Source):
        raise NotImplementedError

    def i_and(self, dest: Destination, *ops: Source):
        raise NotImplementedError

    def i_or(self, dest: Destination, *ops: Source):
        raise NotImplementedError

    def i_dec(self, dest: Destination):
        raise NotImplementedError

    def i_inc(self, dest: Destination):
        raise NotImplementedError

    def i_jmp(self, label: Label):
        raise NotImplementedError

    def i_call(self, label: Label):
        raise NotImplementedError

    def i_mov(self, dest: Destination, src: Source):
        raise NotImplementedError

    def i_ld(self, register: Register, address: Address):
        raise NotImplementedError

    def i_cmp(self, var: Destination, op: Source):
        raise NotImplementedError

    def i_ret(self):
        raise NotImplementedError

    def i_hlt(self):
        raise NotImplementedError

    @classmethod
    def get_all(cls) -> dict[str, Callable]:
        return {
            key.replace('i_', ''): func
            for key, func in cls.__dict__.items()
            if key.startswith('i_')
        }

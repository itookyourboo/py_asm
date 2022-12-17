from typing import Callable

from core.model import Register, Address, Label, Destination, Source, IndirectAddress


class InstructionSet:
    def i_add(self, dest: Destination, *ops: Source) -> None:
        raise NotImplementedError

    def i_sub(self, dest: Destination, *ops: Source) -> None:
        raise NotImplementedError

    def i_mul(self, dest: Destination, *ops: Source) -> None:
        raise NotImplementedError

    def i_div(self, dest: Destination, *ops: Source) -> None:
        raise NotImplementedError

    def i_mod(self, dest: Destination, *ops: Source) -> None:
        raise NotImplementedError

    def i_xor(self, dest: Destination, *ops: Source) -> None:
        raise NotImplementedError

    def i_and(self, dest: Destination, *ops: Source) -> None:
        raise NotImplementedError

    def i_or(self, dest: Destination, *ops: Source) -> None:
        raise NotImplementedError

    def i_dec(self, dest: Destination) -> None:
        raise NotImplementedError

    def i_inc(self, dest: Destination) -> None:
        raise NotImplementedError

    def i_jmp(self, label: Label) -> None:
        raise NotImplementedError

    def i_je(self, label: Label) -> None:
        raise NotImplementedError

    def i_jne(self, label: Label) -> None:
        raise NotImplementedError

    def i_jl(self, label: Label) -> None:
        raise NotImplementedError

    def i_jg(self, label: Label) -> None:
        raise NotImplementedError

    def i_jle(self, label: Label) -> None:
        raise NotImplementedError

    def i_jge(self, label: Label) -> None:
        raise NotImplementedError

    def i_mov(self, dest: Destination, src: Source) -> None:
        raise NotImplementedError

    def i_ld(self, register: Register, address: Address | IndirectAddress) -> None:
        raise NotImplementedError

    def i_cmp(self, var: Destination, op: Source) -> None:
        raise NotImplementedError

    def i_putc(self, op: Source) -> None:
        raise NotImplementedError

    def i_getc(self, dest: Destination) -> None:
        raise NotImplementedError

    def i_putn(self, op: Source) -> None:
        raise NotImplementedError

    def i_getn(self, dest: Destination) -> None:
        raise NotImplementedError

    def i_hlt(self) -> None:
        raise NotImplementedError

    @classmethod
    def get_all(cls) -> dict[str, Callable]:
        return {
            key.replace('i_', ''): func
            for key, func in cls.__dict__.items()
            if key.startswith('i_')
        }

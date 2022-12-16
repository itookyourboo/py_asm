from enum import Enum
from typing import Callable

from core.machine.config import MIN_NUM, MAX_NUM, N_BITS


class Flag(Enum):
    """
    Flag

    - N -- Negative
    - Z -- Zero
    - V -- Overflow
    - C -- Carry
    """
    N = 0
    Z = 1
    V = 2
    C = 3


class ALU:
    def __init__(self):
        self.flags: dict[str, bool] = {
            flag: False
            for flag in Flag.__members__
        }

    def set_flag(self, flag: Flag, value: bool) -> None:
        self.flags[flag.name] = value

    def get_flag(self, flag: Flag) -> bool:
        return self.flags[flag.name]

    def operation(self, operation: Callable, a: int, b: int) -> int:
        result: int = operation(a, b)
        self.set_flag(Flag.N, self._get_sign(result))
        self.set_flag(Flag.Z, self._get_zero(result))
        self.set_flag(Flag.V, self._get_overflow(result))
        self.set_flag(Flag.C, self._get_carry(result))
        return self._strip_number(result)

    def _strip_number(self, number: int) -> int:
        return (
                (-1) * self._get_sign(number) *
                (number & ((1 << N_BITS) - 1))
        )

    def _get_zero(self, number: int) -> bool:
        return number == 0

    def _get_overflow(self, number: int) -> bool:
        return not (MIN_NUM <= number <= MAX_NUM)

    def _get_sign(self, number: int) -> bool:
        return bool(number & (1 << (N_BITS - 1)))

    def _get_carry(self, number: int) -> bool:
        return bool(number & (1 << N_BITS))

    def __str__(self) -> str:
        return str(self.flags)

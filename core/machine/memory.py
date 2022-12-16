from core.exceptions import DataNotFound
from core.model import Address

from .arithmetic import _strip_number
from ..config import MEMORY_SIZE


class MemoryController:
    def __init__(self, data: list[int]) -> None:
        self.data = data
        # self.data.extend(
        #     [0 for _ in range(MEMORY_SIZE - len(data))]
        # )

    def _check_bounds(self, address: Address) -> None:
        if not (0 <= address.index <= len(self.data)):
            raise DataNotFound(
                f'Cannot get address {address.index}'
            )

    def get(self, address: Address) -> int:
        self._check_bounds(address)
        return self.data[address.index]

    def set(self, address: Address, value: int | str) -> None:
        self._check_bounds(address)
        self.data[address.index] = _strip_number(value)

    def __repr__(self) -> str:
        return str(self.data)

from core.exceptions import DataNotFound, IncorrectDataType
from core.model import Constant, String, Number, Address


class MemoryController:
    def __init__(self, data: dict[str, Constant]) -> None:
        self.data = data

    def get(self, address: Address) -> int | str:
        if address.value not in self.data:
            raise DataNotFound(address.value)
        return self.data[address.value].value

    def set(self, address: Address, value: int | str) -> None:
        const: Constant = self.data[address.value]
        if (
                isinstance(const, Number) and not isinstance(value, int)
                or
                isinstance(const, String) and not isinstance(value, str)
        ):
            raise IncorrectDataType(type(const))
        const.value = value

    def __repr__(self) -> str:
        return str({key: const.value for key, const in self.data.items()})

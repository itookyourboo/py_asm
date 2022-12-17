from typing import Iterator, Optional

from core.config import NULL_TERM


class IOController:
    def __init__(self):
        self.stdin: Optional[Iterator] = None

    def putc(self, char: int) -> None:
        print(chr(char), end='')

    def _getc(self) -> Iterator[int]:
        yield from map(ord, input() + '\n')
        yield NULL_TERM

    def getc(self) -> int:
        if self.stdin is None:
            self.stdin = iter(self._getc())

        try:
            return next(self.stdin)
        except StopIteration:
            self.stdin = None
            return NULL_TERM

    def putn(self, number: int) -> None:
        print(number, end='')

    def getn(self) -> int:
        result: int = int(''.join(map(chr, self._getc())).strip())
        return result

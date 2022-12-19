"""
Input-Output Unit
"""

import sys
from typing import Iterator, Optional

from core.machine.config import NULL_TERM


class IOController:
    """
    Input-Output Controller class
    """

    def __init__(self) -> None:
        self.stdin: Optional[Iterator] = None
        self.stdout: Optional[Iterator] = None

    def putc(self, char: int) -> None:
        """
        Puts symbol into stdout
        """
        print(chr(char), end='')

    def _getc(self) -> Iterator[int]:
        """
        Generate symbol codes stream from input string
        """
        yield from map(ord, sys.stdin.read())
        yield NULL_TERM

    def getc(self) -> int:
        """
        Get symbol from stdout
        """
        if self.stdin is None:
            self.stdin = iter(self._getc())

        try:
            return next(self.stdin)
        except StopIteration:
            self.stdin = None
            return NULL_TERM

    def putn(self, number: int) -> None:
        """
        Put number into stdout
        """
        print(number, end='')

    def getn(self) -> int:
        """
        Get number from stdout
        """
        number: str = ''.join(map(chr, self._getc()))
        result: int = int(number.strip('\x00'))
        return result

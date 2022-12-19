"""
Clock Generator Unit
"""


class ClockGenerator:
    """
    Clock Generator class
        - _tick  -- number of ticks
        - _inst  -- number of instructions
    """
    def __init__(self) -> None:
        self._tick = 0
        self._inst = 0

    def tick(self) -> None:
        """
        Increment ticks count
        """
        self._tick += 1

    def inst(self) -> None:
        """
        Increment instructions count
        """
        self._inst += 1

    def __str__(self) -> str:
        return f'tick: {self._tick}, inst: {self._inst}'

class ClockGenerator:
    def __init__(self):
        self._tick = 0

    def tick(self):
        self._tick += 1

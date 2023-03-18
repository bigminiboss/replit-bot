from typing import Any


class Switch:
    def __init__(self, name: Any):
        self.n = name

    def case(self, current: Any) -> bool:
        return self.n == current

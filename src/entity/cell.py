"""Entity — Cell (E-2, E-5, INV-5)."""

from __future__ import annotations


class Cell:
    def __init__(self, value: int, row: int, col: int) -> None:
        self.value = value
        self.row = row
        self.col = col
        self.state = "empty" if value == 0 else "filled"  # INV-5, E-5

    def is_empty(self) -> bool:
        return self.value == 0  # E-5

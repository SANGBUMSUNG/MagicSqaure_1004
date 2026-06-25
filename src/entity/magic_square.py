"""Entity — MagicSquare (E-1, E-4, INV-1, INV-2)."""

from __future__ import annotations

from entity.cell import Cell


class MagicSquare:
    MAGIC_SUM = 34  # INV-2
    SIZE = 4
    FULL_VALUES = frozenset(range(1, 17))  # INV-3

    def __init__(self, cells: list[Cell]) -> None:
        if len(cells) != self.SIZE * self.SIZE:  # INV-1
            raise ValueError("MagicSquare requires exactly 16 cells")
        self.cells = cells
        self.size = self.SIZE

    @classmethod
    def from_grid(cls, grid: list[list[int]]) -> MagicSquare:
        if len(grid) != cls.SIZE or any(len(row) != cls.SIZE for row in grid):  # E-4, INV-1
            raise ValueError("Grid must be 4x4")
        cells = [
            Cell(grid[row][col], row, col)
            for row in range(cls.SIZE)
            for col in range(cls.SIZE)
        ]  # INV-7
        return cls(cells)

    def get_cell(self, row: int, col: int) -> Cell:
        return self.cells[row * self.SIZE + col]

    def to_grid(self) -> list[list[int]]:
        grid = [[0] * self.SIZE for _ in range(self.SIZE)]
        for cell in self.cells:
            grid[cell.row][cell.col] = cell.value
        return grid

    def with_value(self, row: int, col: int, value: int) -> MagicSquare:
        grid = self.to_grid()
        grid[row][col] = value
        return MagicSquare.from_grid(grid)

    def blank_positions(self) -> list[tuple[int, int]]:
        return [(cell.row, cell.col) for cell in self.cells if cell.is_empty()]

    def filled_values(self) -> list[int]:
        return [cell.value for cell in self.cells if not cell.is_empty()]

    def iter_line_sums(self) -> list[tuple[str, int]]:
        """행4 + 열4 + 대각2 = 10선분 (INV-4)."""
        grid = self.to_grid()
        checks: list[tuple[str, int]] = []

        for row in range(self.size):
            checks.append((f"row_{row}", sum(grid[row])))

        for col in range(self.size):
            checks.append((f"col_{col}", sum(grid[r][col] for r in range(self.size))))

        checks.append(("diag_main", sum(grid[i][i] for i in range(self.size))))
        checks.append(
            ("diag_anti", sum(grid[i][self.size - 1 - i] for i in range(self.size)))
        )
        return checks

    def has_full_value_set(self) -> bool:
        return set(self.filled_values()) == self.FULL_VALUES  # INV-3

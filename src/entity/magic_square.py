"""Entity — MagicSquare (E-1, E-4, INV-1, INV-2)."""

from __future__ import annotations

from entity.cell import Cell


class MagicSquare:
  MAGIC_SUM = 34  # INV-2
  SIZE = 4

  def __init__(self, cells: list[Cell]) -> None:
    if len(cells) != 16:  # INV-1
      raise ValueError("MagicSquare requires exactly 16 cells")
    self.cells = cells
    self.size = self.SIZE

  @classmethod
  def from_grid(cls, grid: list[list[int]]) -> MagicSquare:
    if len(grid) != cls.SIZE or any(len(row) != cls.SIZE for row in grid):  # E-4, INV-1
      raise ValueError("Grid must be 4x4")
    cells: list[Cell] = []
    for row in range(cls.SIZE):
      for col in range(cls.SIZE):
        cells.append(Cell(grid[row][col], row, col))  # INV-7
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

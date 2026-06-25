"""Control — SquareValidator (C-3, INV-3, INV-4, F1~F4)."""

from __future__ import annotations

from entity.magic_square import MagicSquare
from entity.solve_result import SolveResult


class SquareValidator:
  def validate(self, square: MagicSquare) -> SolveResult:
    blank_positions = [
      (cell.row, cell.col) for cell in square.cells if cell.is_empty()
    ]
    if blank_positions:
      return SolveResult(
        blank_positions=blank_positions,
        is_complete=False,
        failure_codes=["F3"],
        failed_lines=[],
      )  # F3, AC-4

    values = [cell.value for cell in square.cells]
    failure_codes: list[str] = []
    failed_lines: list[str] = []

    if sorted(values) != list(range(1, 17)):
      failure_codes.append("F4")  # INV-3, AC-5

    line_checks = self._line_checks(square)
    for line_id, total in line_checks:
      if total != MagicSquare.MAGIC_SUM:
        failed_lines.append(line_id)  # INV-4, AC-2, AC-3

    is_complete = not failure_codes and not failed_lines
    return SolveResult(
      blank_positions=blank_positions,
      is_complete=is_complete,
      failure_codes=failure_codes,
      failed_lines=failed_lines,
    )  # C-3

  def _line_checks(self, square: MagicSquare) -> list[tuple[str, int]]:
    grid = square.to_grid()
    size = square.size
    checks: list[tuple[str, int]] = []

    for row in range(size):
      checks.append((f"row_{row}", sum(grid[row])))  # INV-4

    for col in range(size):
      checks.append((f"col_{col}", sum(grid[r][col] for r in range(size))))

    diag_main = sum(grid[i][i] for i in range(size))
    checks.append(("diag_main", diag_main))

    diag_anti = sum(grid[i][size - 1 - i] for i in range(size))
    checks.append(("diag_anti", diag_anti))

    return checks

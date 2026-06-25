"""Control — Solver (C-2, AC-1)."""

from __future__ import annotations

from control.missing_finder import MissingFinder
from entity.magic_square import MagicSquare


class Solver:
    def solve(self, square: MagicSquare) -> MagicSquare:
        blanks = MissingFinder().find(square)
        grid = square.to_grid()
        missing_numbers = sorted(MagicSquare.FULL_VALUES - set(square.filled_values()))  # INV-3

        candidates = {
            (row, col): self._candidates_for_blank(grid, row, col)
            for row, col in blanks
        }
        assignment = self._assign_blanks(blanks, candidates, missing_numbers)

        result = square
        for (row, col), value in assignment.items():
            result = result.with_value(row, col, value)  # C-2, AC-1
        return result

    def _candidates_for_blank(
        self, grid: list[list[int]], row: int, col: int
    ) -> set[int]:
        size = MagicSquare.SIZE
        row_sum = sum(grid[row][c] for c in range(size) if c != col)
        col_sum = sum(grid[r][col] for r in range(size) if r != row)
        return {MagicSquare.MAGIC_SUM - row_sum, MagicSquare.MAGIC_SUM - col_sum}

    def _assign_blanks(
        self,
        blanks: list[tuple[int, int]],
        candidates: dict[tuple[int, int], set[int]],
        missing_numbers: list[int],
    ) -> dict[tuple[int, int], int]:
        if len(blanks) == 1:
            row, col = blanks[0]
            for value in missing_numbers:
                if value in candidates[(row, col)]:
                    return {(row, col): value}
            raise ValueError("No valid value for blank")

        if len(blanks) == 2:
            return self._solve_two_blanks(blanks, candidates, missing_numbers)

        raise ValueError(f"Unsupported blank count: {len(blanks)}")

    def _solve_two_blanks(
        self,
        blanks: list[tuple[int, int]],
        candidates: dict[tuple[int, int], set[int]],
        missing_numbers: list[int],
    ) -> dict[tuple[int, int], int]:
        (r1, c1), (r2, c2) = blanks
        for a in missing_numbers:
            for b in missing_numbers:
                if a == b:
                    continue
                if a in candidates[(r1, c1)] and b in candidates[(r2, c2)]:
                    return {(r1, c1): a, (r2, c2): b}
                if b in candidates[(r1, c1)] and a in candidates[(r2, c2)]:
                    return {(r1, c1): b, (r2, c2): a}
        raise ValueError("No valid assignment for blanks")

"""Control — SquareValidator (C-3, INV-3, INV-4, F1~F4)."""

from __future__ import annotations

from entity.magic_square import MagicSquare
from entity.solve_result import SolveResult


class SquareValidator:
    def validate(self, square: MagicSquare) -> SolveResult:
        blank_positions = square.blank_positions()
        if blank_positions:
            return SolveResult(
                blank_positions=blank_positions,
                is_complete=False,
                failure_codes=["F3"],
                failed_lines=[],
            )  # F3, AC-4

        failure_codes: list[str] = []
        failed_lines: list[str] = []

        if not square.has_full_value_set():
            failure_codes.append("F4")  # INV-3, AC-5

        for line_id, total in square.iter_line_sums():
            if total != MagicSquare.MAGIC_SUM:
                failed_lines.append(line_id)  # INV-4, AC-2, AC-3

        is_complete = not failure_codes and not failed_lines
        return SolveResult(
            blank_positions=blank_positions,
            is_complete=is_complete,
            failure_codes=failure_codes,
            failed_lines=failed_lines,
        )  # C-3

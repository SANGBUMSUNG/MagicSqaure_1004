"""Boundary — ResultDisplay (B-3, AC-2, AC-3, AC-6)."""

from __future__ import annotations

from entity.solve_result import SolveResult


class ResultDisplay:
    def show(self, result: SolveResult) -> str:
        parts: list[str] = []

        if result.is_complete:
            parts.append("완료 (complete)")  # AC-1, AC-6
        else:
            parts.append("미완료 (incomplete)")

        for code in result.failure_codes:
            parts.append(f"failure_code: {code}")  # B-3, AC-5

        for line in result.failed_lines:
            parts.append(f"failed_line: {line}")  # B-3, AC-2, AC-3
            if "diag" in line:
                parts.append("대각선(diag) 불일치")  # AC-2

        for row, col in result.blank_positions:
            parts.append(f"blank: ({row}, {col})")  # AC-4

        return "\n".join(parts)  # B-3

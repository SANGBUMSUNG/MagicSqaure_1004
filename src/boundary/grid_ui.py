"""Boundary — GridUI (B-1, E-1, E-2)."""

from __future__ import annotations


class GridUI:
    def render(self, grid: list[list[int]]) -> str:
        lines: list[str] = []
        for row in grid:
            cells = [str(value) if value != 0 else "0" for value in row]
            lines.append(" ".join(f"{cell:>2}" for cell in cells))
        return "\n".join(lines)  # B-1

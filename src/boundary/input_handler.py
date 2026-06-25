"""Boundary — InputHandler (B-2, E-4)."""

from __future__ import annotations

from entity.magic_square import MagicSquare


class InputHandler:
    @staticmethod
    def read_grid(grid: list[list[int]]) -> MagicSquare:
        return MagicSquare.from_grid(grid)  # B-2, E-4

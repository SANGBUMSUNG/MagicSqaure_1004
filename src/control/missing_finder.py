"""Control — MissingFinder (C-1, INV-6)."""

from __future__ import annotations

from entity.magic_square import MagicSquare


class MissingFinder:
    def find(self, square: MagicSquare) -> list[tuple[int, int]]:
        return square.blank_positions()  # C-1, INV-6

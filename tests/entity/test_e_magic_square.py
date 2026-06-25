"""E-1, E-4 — docs/Test-Plan.md §4.2"""

import pytest

from entity.magic_square import MagicSquare

from grids import PUZZLE_GRID


class TestE1MagicSquare:
    """E-1: MagicSquare 구조 계약."""

    def test_magic_square_has_cells_and_constants(self):
        square = MagicSquare.from_grid(PUZZLE_GRID)
        assert square.size == 4
        assert square.MAGIC_SUM == 34
        assert len(square.cells) == 16


class TestE4FromGrid:
    """E-4: from_grid 팩토리."""

    def test_from_grid_valid_4x4(self):
        square = MagicSquare.from_grid(PUZZLE_GRID)
        assert isinstance(square, MagicSquare)

    def test_from_grid_rejects_invalid_size(self):
        invalid = [[1] * 5 for _ in range(5)]
        with pytest.raises(ValueError):
            MagicSquare.from_grid(invalid)

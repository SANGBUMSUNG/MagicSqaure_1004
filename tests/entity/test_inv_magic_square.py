"""INV-1 ~ INV-4 — docs/Test-Plan.md §4.1"""

import pytest

from control.square_validator import SquareValidator
from entity.magic_square import MagicSquare
from grids import PUZZLE_GRID, SOLVED_GRID


class TestInv1GridSize:
    """INV-1: 격자는 항상 4×4 (16칸)."""

    def test_grid_is_4x4(self):
        square = MagicSquare.from_grid(PUZZLE_GRID)
        assert square.size == 4
        assert len(square.cells) == 16

    def test_reject_non_4x4_grid(self):
        invalid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        with pytest.raises(ValueError):
            MagicSquare.from_grid(invalid)


class TestInv2MagicSum:
    """INV-2: MAGIC_SUM = 34."""

    def test_magic_sum_is_34(self):
        assert MagicSquare.MAGIC_SUM == 34


class TestInv3UniqueNumbers:
    """INV-3: 완성 격자에서 1~16 각 1회."""

    def test_solved_uses_1_to_16_once(self):
        square = MagicSquare.from_grid(SOLVED_GRID)
        values = [cell.value for cell in square.cells]
        assert sorted(values) == list(range(1, 17))


class TestInv4TenLines:
    """INV-4: 행4+열4+대각2 = 10선분 합 34."""

    def test_solved_all_10_lines_sum_34(self):
        square = MagicSquare.from_grid(SOLVED_GRID)
        result = SquareValidator().validate(square)
        assert result.is_complete is True
        assert result.failed_lines == []

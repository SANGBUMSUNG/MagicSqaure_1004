"""C-1 — INV-6, AC-4 — docs/Test-Plan.md §4.1, §5"""

from control.missing_finder import MissingFinder
from entity.magic_square import MagicSquare

from grids import BLANK_POSITIONS, PUZZLE_GRID


class TestC1MissingFinder:
    """C-1: 빈칸 위치 탐색."""

    def test_puzzle_has_exactly_two_blanks(self):
        """INV-6: 퍼즐 입력 빈칸 2개."""
        square = MagicSquare.from_grid(PUZZLE_GRID)
        blanks = MissingFinder().find(square)
        assert len(blanks) == 2

    def test_find_two_blank_positions(self):
        square = MagicSquare.from_grid(PUZZLE_GRID)
        blanks = MissingFinder().find(square)
        assert set(blanks) == set(BLANK_POSITIONS)

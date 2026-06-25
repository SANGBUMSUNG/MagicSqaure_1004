"""B-2 — E-4 — docs/Test-Plan.md §6.2"""

from boundary.input_handler import InputHandler
from entity.magic_square import MagicSquare

from grids import PUZZLE_GRID


class TestB2InputHandler:
    """B-2: 격자 입력 수신."""

    def test_read_grid_from_literal(self):
        square = InputHandler.read_grid(PUZZLE_GRID)
        assert isinstance(square, MagicSquare)
        assert square.size == 4

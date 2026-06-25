"""C-2, AC-1 — docs/Test-Plan.md §5"""

from control.missing_finder import MissingFinder
from control.solver import Solver
from control.square_validator import SquareValidator
from entity.magic_square import MagicSquare

from grids import EXPECTED_VALUES, PUZZLE_GRID


class TestC2Solver:
    """C-2: 빈칸 값 계산."""

    def test_solver_fills_example_blanks(self):
        square = MagicSquare.from_grid(PUZZLE_GRID)
        solved = Solver().solve(square)
        for (row, col), expected in EXPECTED_VALUES.items():
            cell = solved.get_cell(row, col)
            assert cell.value == expected


class TestAc1Integration:
    """AC-1: find → solve → validate 통합."""

    def test_solve_then_validate_complete(self):
        square = MagicSquare.from_grid(PUZZLE_GRID)
        blanks = MissingFinder().find(square)
        assert len(blanks) == 2

        solved = Solver().solve(square)
        result = SquareValidator().validate(solved)

        assert result.is_complete is True
        assert result.is_success() is True

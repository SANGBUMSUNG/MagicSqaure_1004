"""B-3 — AC-2, AC-3, AC-6 — docs/Test-Plan.md §6.2"""

from boundary.result_display import ResultDisplay
from control.square_validator import SquareValidator
from entity.magic_square import MagicSquare
from entity.solve_result import SolveResult

from grids import ROWS_COLS_ONLY_GRID


class TestB3ResultDisplay:
    """B-3: failure_codes, failed_lines 출력."""

    def test_show_failure_codes_and_lines(self):
        square = MagicSquare.from_grid(ROWS_COLS_ONLY_GRID)
        result = SquareValidator().validate(square)
        output = ResultDisplay().show(result)
        assert isinstance(output, str)
        assert len(output) > 0

    def test_show_explicit_failure_result(self):
        result = SolveResult(
            blank_positions=[],
            filled_values=[],
            is_complete=False,
            failure_codes=["F1"],
            failed_lines=["diag_main"],
        )
        output = ResultDisplay().show(result)
        assert "F1" in output
        assert "diag_main" in output

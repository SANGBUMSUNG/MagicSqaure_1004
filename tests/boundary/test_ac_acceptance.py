"""AC-1 ~ AC-6 — US-1~3 — docs/Test-Plan.md §6.1"""

from boundary.input_handler import InputHandler
from boundary.result_display import ResultDisplay
from control.missing_finder import MissingFinder
from control.solver import Solver
from control.square_validator import SquareValidator
from entity.magic_square import MagicSquare

from grids import (
    BLANK_REMAINING_GRID,
    DUPLICATE_GRID,
    PUZZLE_GRID,
    ROWS_COLS_ONLY_GRID,
)


class TestAc1Us1ExamplePuzzle:
    """AC-1, US-1: 예시 격자 → 풀이 → 완료."""

    def test_us1_example_puzzle_complete(self):
        square = InputHandler.read_grid(PUZZLE_GRID)
        solved = Solver().solve(square)
        result = SquareValidator().validate(solved)
        output = ResultDisplay().show(result)
        assert result.is_complete is True
        assert "complete" in output.lower() or "완료" in output


class TestAc2Us2DiagonalFailure:
    """AC-2, US-2: 대각선 실패 표시."""

    def test_us2_diagonal_failure_shown(self):
        square = MagicSquare.from_grid(ROWS_COLS_ONLY_GRID)
        result = SquareValidator().validate(square)
        output = ResultDisplay().show(result)
        assert result.is_complete is False
        assert "diag" in output.lower() or "대각" in output


class TestAc3FailedLinesListed:
    """AC-3, US-2: 실패 선분 목록."""

    def test_us2_failed_lines_listed(self):
        square = MagicSquare.from_grid(ROWS_COLS_ONLY_GRID)
        result = SquareValidator().validate(square)
        output = ResultDisplay().show(result)
        for line in result.failed_lines:
            assert line in output or line.replace("_", " ") in output


class TestAc4BlankRemaining:
    """AC-4, F3: 빈칸 잔존."""

    def test_blank_remaining_reported(self):
        square = MagicSquare.from_grid(BLANK_REMAINING_GRID)
        result = SquareValidator().validate(square)
        output = ResultDisplay().show(result)
        assert result.is_complete is False
        assert result.blank_positions


class TestAc5NumberSetError:
    """AC-5, F4: 숫자 집합 오류."""

    def test_number_set_error_reported(self):
        square = MagicSquare.from_grid(DUPLICATE_GRID)
        result = SquareValidator().validate(square)
        output = ResultDisplay().show(result)
        assert result.is_complete is False
        assert result.failure_codes


class TestAc6Us3Revalidate:
    """AC-6, US-3: 수정 후 재검증."""

    def test_us3_revalidate_after_edit(self):
        square = MagicSquare.from_grid(DUPLICATE_GRID)
        first = SquareValidator().validate(square)
        assert first.is_complete is False

        fixed = MagicSquare.from_grid(PUZZLE_GRID)
        solved = Solver().solve(fixed)
        second = SquareValidator().validate(solved)
        output = ResultDisplay().show(second)
        assert second.is_complete is True
        assert "complete" in output.lower() or "완료" in output

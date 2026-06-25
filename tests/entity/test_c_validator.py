"""C-3 — F1~F4, AC-2~AC-5 — docs/Test-Plan.md §4.3, §5"""

from control.square_validator import SquareValidator
from entity.magic_square import MagicSquare

from grids import (
    BLANK_REMAINING_GRID,
    DUPLICATE_GRID,
    ROWS_COLS_ONLY_GRID,
    SOLVED_GRID,
)


class TestC3SquareValidator:
    """C-3: SquareValidator — 10선분 + 숫자 집합 검사."""

    def test_rows_cols_ok_diagonal_fails(self):
        """F1, AC-2: 행·열만 34, 대각선 불일치 → 미완료."""
        square = MagicSquare.from_grid(ROWS_COLS_ONLY_GRID)
        result = SquareValidator().validate(square)
        assert result.is_complete is False
        assert any("diag" in line for line in result.failed_lines)

    def test_reports_all_failed_lines(self):
        """F2, AC-3: 불일치 선분 전부 failed_lines에 포함."""
        square = MagicSquare.from_grid(ROWS_COLS_ONLY_GRID)
        result = SquareValidator().validate(square)
        assert len(result.failed_lines) >= 1

    def test_duplicate_numbers_fail(self):
        """F4, AC-5: 1~16 중복 → 집합 오류."""
        square = MagicSquare.from_grid(DUPLICATE_GRID)
        result = SquareValidator().validate(square)
        assert result.is_complete is False
        assert any("F4" in code or "SET" in code for code in result.failure_codes)

    def test_solved_grid_passes(self):
        """INV-3, INV-4: 완성 격자 통과."""
        square = MagicSquare.from_grid(SOLVED_GRID)
        result = SquareValidator().validate(square)
        assert result.is_complete is True

    def test_blank_remaining_incomplete(self):
        """F3, AC-4: 빈칸(0) 잔존 → 미완료 + 좌표."""
        square = MagicSquare.from_grid(BLANK_REMAINING_GRID)
        result = SquareValidator().validate(square)
        assert result.is_complete is False
        assert len(result.blank_positions) >= 1

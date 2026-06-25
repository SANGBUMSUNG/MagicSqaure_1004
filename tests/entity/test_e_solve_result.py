"""E-3, E-6 — docs/Test-Plan.md §4.2"""

from entity.solve_result import SolveResult


class TestE3SolveResultFields:
    """E-3: SolveResult 필드 계약."""

    def test_solve_result_fields(self):
        result = SolveResult(
            blank_positions=[(1, 3), (2, 2)],
            filled_values=[8, 7],
            is_complete=False,
            failure_codes=[],
            failed_lines=[],
        )
        assert result.blank_positions == [(1, 3), (2, 2)]
        assert result.filled_values == [8, 7]
        assert result.is_complete is False
        assert result.failure_codes == []
        assert result.failed_lines == []


class TestE6IsSuccess:
    """E-6: is_success() 행위."""

    def test_is_success_when_complete_no_failures(self):
        result = SolveResult(
            blank_positions=[],
            filled_values=[],
            is_complete=True,
            failure_codes=[],
            failed_lines=[],
        )
        assert result.is_success() is True

    def test_is_success_false_with_failure_codes(self):
        result = SolveResult(
            blank_positions=[],
            filled_values=[],
            is_complete=False,
            failure_codes=["F4"],
            failed_lines=[],
        )
        assert result.is_success() is False

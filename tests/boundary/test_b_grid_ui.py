"""B-1 — docs/Test-Plan.md §6.2"""

from boundary.grid_ui import GridUI

from grids import PUZZLE_GRID


class TestB1GridUI:
    """B-1: 4×4 격자 텍스트 표시."""

    def test_render_4x4_text(self):
        output = GridUI().render(PUZZLE_GRID)
        lines = output.strip().splitlines()
        assert len(lines) == 4
        assert "0" in output or "." in output

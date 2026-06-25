"""E-2, E-5 — INV-5, INV-7 — docs/Test-Plan.md §4.1, §4.2"""

from entity.cell import Cell
from entity.magic_square import MagicSquare

from grids import PUZZLE_GRID


class TestE2CellAttributes:
    """E-2: Cell 속성 계약."""

    def test_cell_has_required_attributes(self):
        cell = Cell(value=5, row=1, col=2)
        assert cell.value == 5
        assert cell.row == 1
        assert cell.col == 2
        assert cell.state in ("empty", "filled")


class TestE5IsEmpty:
    """E-5, INV-5: value == 0 ⇔ empty."""

    def test_zero_means_empty_state(self):
        cell = Cell(value=0, row=1, col=3)
        assert cell.is_empty() is True
        assert cell.state == "empty"

    def test_is_empty_equivalence(self):
        empty = Cell(value=0, row=0, col=0)
        filled = Cell(value=5, row=0, col=0)
        assert empty.is_empty() is True
        assert filled.is_empty() is False
        assert filled.state == "filled"


class TestInv7CellCoords:
    """INV-7: row, col ∈ {0,1,2,3}."""

    def test_cell_coords_in_range(self):
        square = MagicSquare.from_grid(PUZZLE_GRID)
        for cell in square.cells:
            assert 0 <= cell.row <= 3
            assert 0 <= cell.col <= 3

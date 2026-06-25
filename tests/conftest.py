"""pytest 공통 fixture."""

import pytest

from grids import (
    BLANK_REMAINING_GRID,
    DUPLICATE_GRID,
    PUZZLE_GRID,
    ROWS_COLS_ONLY_GRID,
    SOLVED_GRID,
)


@pytest.fixture
def puzzle_grid():
    return [row[:] for row in PUZZLE_GRID]


@pytest.fixture
def solved_grid():
    return [row[:] for row in SOLVED_GRID]


@pytest.fixture
def rows_cols_only_grid():
    return [row[:] for row in ROWS_COLS_ONLY_GRID]


@pytest.fixture
def duplicate_grid():
    return [row[:] for row in DUPLICATE_GRID]


@pytest.fixture
def blank_remaining_grid():
    return [row[:] for row in BLANK_REMAINING_GRID]

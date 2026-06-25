"""pytest 공통 fixture."""

import sys
from pathlib import Path

# src/ 를 import 경로에 추가 (entity, control, boundary)
_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

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

"""공통 테스트 데이터 — docs/Test-Plan.md §3."""

# §3.1 PUZZLE_GRID (AC-1)
PUZZLE_GRID = [
    [16, 3, 2, 13],
    [5, 10, 11, 0],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]
BLANK_POSITIONS = [(1, 3), (2, 2)]
EXPECTED_VALUES = {(1, 3): 8, (2, 2): 7}

# §3.2 SOLVED_GRID (INV-3, INV-4)
SOLVED_GRID = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

# §3.3 ROWS_COLS_ONLY_GRID (F1, AC-2) — 행·열 34, 주대각선 ≠ 34
ROWS_COLS_ONLY_GRID = [
    [2, 13, 3, 16],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

# §3.4 DUPLICATE_GRID (F4, AC-5)
DUPLICATE_GRID = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 16],
]

# §3.5 BLANK_REMAINING_GRID (F3, AC-4)
BLANK_REMAINING_GRID = PUZZLE_GRID

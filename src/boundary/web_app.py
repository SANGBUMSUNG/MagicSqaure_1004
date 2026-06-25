"""Boundary — Flask 웹 UI (B-1~B-3 브라우저)."""

from __future__ import annotations

from pathlib import Path

from flask import Flask, render_template, request

from boundary.input_handler import InputHandler
from boundary.result_display import ResultDisplay
from control.missing_finder import MissingFinder
from control.solver import Solver
from control.square_validator import SquareValidator
from entity.magic_square import MagicSquare

EXAMPLE_GRID = [
    [16, 3, 2, 13],
    [5, 10, 11, 0],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]

DUPLICATE_EXAMPLE = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 16],
]

ROWS_COLS_ONLY_EXAMPLE = [
    [2, 13, 3, 16],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]


def create_app() -> Flask:
    template_dir = Path(__file__).resolve().parent / "templates"
    app = Flask(__name__, template_folder=str(template_dir))

    @app.get("/")
    def index():
        return _render_page(EXAMPLE_GRID)

    @app.post("/")
    def handle_action():
        action = request.form.get("action", "validate")
        if action == "example":
            return _render_page(EXAMPLE_GRID, info="예시 퍼즐을 불러왔습니다.")
        if action == "duplicate":
            return _render_page(DUPLICATE_EXAMPLE, info="중복 숫자 예시 (F4 테스트).")
        if action == "diagonal_fail":
            return _render_page(
                ROWS_COLS_ONLY_EXAMPLE,
                info="대각선 불일치 예시 (AC-2 테스트).",
            )

        try:
            grid = _grid_from_form(request.form)
        except ValueError as exc:
            return _render_page(EXAMPLE_GRID, error=str(exc))

        try:
            square = InputHandler.read_grid(grid)
        except ValueError as exc:
            return _render_page(grid, error=str(exc))

        if action == "solve":
            blanks = MissingFinder().find(square)
            solved = Solver().solve(square)
            result = SquareValidator().validate(solved)
            return _render_page(
                solved.to_grid(),
                result=result,
                blanks=blanks,
                info="빈칸을 채운 뒤 검증했습니다.",
            )

        result = SquareValidator().validate(square)
        return _render_page(grid, result=result)

    return app


def _grid_from_form(form) -> list[list[int]]:
    grid: list[list[int]] = []
    for row in range(MagicSquare.SIZE):
        line: list[int] = []
        for col in range(MagicSquare.SIZE):
            raw = form.get(f"cell_{row}_{col}", "").strip()
            if raw == "":
                line.append(0)
                continue
            value = int(raw)
            if value < 0 or value > 16:
                raise ValueError("각 칸은 0(빈칸) 또는 1~16 사이여야 합니다.")
            line.append(value)
        grid.append(line)
    return grid


def _render_page(
    grid: list[list[int]],
    *,
    result=None,
    blanks: list[tuple[int, int]] | None = None,
    error: str | None = None,
    info: str | None = None,
):
    display = ResultDisplay().show(result) if result is not None else None
    return render_template(
        "index.html",
        grid=grid,
        size=MagicSquare.SIZE,
        magic_sum=MagicSquare.MAGIC_SUM,
        result=result,
        display=display,
        blanks=blanks or [],
        error=error,
        info=info,
    )

# Test Plan — MagicSquare_1004

| 항목 | 내용 |
|------|------|
| 버전 | v0.1 |
| 작성일 | 2026-06-25 |
| 단계 | RED (실패 테스트 선행) |
| 근거 | [PRD.md](./PRD.md), [README.md](../README.md) §RED 체크리스트 |

---

## 1. 목적

본 문서는 v0 **RED 단계**에서 작성할 pytest 테스트 계획이다.  
모든 테스트는 [PRD](./PRD.md)의 계약 ID(`INV-*`, `E-*`, `AC-*`, `C-*`, `B-*`)를 추적하며, **구현 전에 실패**해야 한다.

### 1.1 범위

| 포함 | 제외 |
|------|------|
| INV-1~7, E-1~6, C-1~3, AC-1~6, B-1~3 | 3×3 / 5×5 일반화 |
| 예시 격자·Mom Test 재현 데이터 | 웹 UI · 게임화 |
| `tests/entity/`, `tests/boundary/` | GREEN 구현 (`src/`) |

### 1.2 성공 기준 (RED 완료)

- [ ] 계획된 테스트 케이스가 `tests/`에 존재
- [ ] `pytest -q` 실행 시 **의도적 실패** (ImportError 또는 AssertionError)
- [ ] 각 테스트에 계약 ID가 이름·docstring·주석으로 명시
- [ ] 커밋 메시지: `test(RED): <계약 ID 목록>`

---

## 2. 테스트 구조

```
tests/
├── conftest.py              # 공통 fixture (예시 격자, 완성 격자)
├── entity/
│   test_inv_magic_square.py # INV-1 ~ INV-7
│   test_e_cell.py           # E-2, E-5, INV-5, INV-7
│   test_e_magic_square.py   # E-1, E-4, INV-1, INV-2
│   test_e_solve_result.py  # E-3, E-6
│   test_c_validator.py      # C-3, F1~F4, AC-2,3,5
│   test_c_missing_finder.py # C-1, INV-6, AC-4
│   └── test_c_solver.py     # C-2, AC-1
└── boundary/
    ├── test_ac_acceptance.py # AC-1 ~ AC-6, US-1~3
    ├── test_b_grid_ui.py     # B-1
    ├── test_b_input_handler.py # B-2
    └── test_b_result_display.py # B-3
```

### 2.1 실행 명령

```bash
pytest tests/entity -q      # M1, M2
pytest tests/boundary -q    # M3
pytest -q                     # 전체
```

---

## 3. 공통 테스트 데이터 (Fixture)

좌표는 **0-based** (`row, col ∈ {0,1,2,3}`).

### 3.1 `PUZZLE_GRID` — 예시 퍼즐 (AC-1)

```python
PUZZLE_GRID = [
    [16,  3,  2, 13],
    [ 5, 10, 11,  0],   # blank at (1, 3) → 8
    [ 9,  6,  0, 12],   # blank at (2, 2) → 7
    [ 4, 15, 14,  1],
]
BLANK_POSITIONS = [(1, 3), (2, 2)]
EXPECTED_VALUES = { (1, 3): 8, (2, 2): 7 }
```

### 3.2 `SOLVED_GRID` — 완성 격자 (INV-3, INV-4)

```python
SOLVED_GRID = [
    [16,  3,  2, 13],
    [ 5, 10, 11,  8],
    [ 9,  6,  7, 12],
    [ 4, 15, 14,  1],
]
```

### 3.3 `ROWS_COLS_ONLY_GRID` — Mom Test F1 (AC-2)

행·열만 34, **대각선 불일치**인 인위적 격자 (테스트 작성 시 구성).

### 3.4 `DUPLICATE_GRID` — F4 (AC-5)

1~16 중복이 있는 격자.

### 3.5 `BLANK_REMAINING_GRID` — F3 (AC-4)

0이 1개 이상 남은 미완성 격자.

---

## 4. M1 — Entity · Validator

경로: `tests/entity/`

### 4.1 불변식 (INV)

| ID | 테스트 파일 | 테스트 함수 (제안) | 입력 | 기대 결과 |
|----|-------------|-------------------|------|-----------|
| INV-1 | `test_inv_magic_square.py` | `test_grid_is_4x4` | `MagicSquare.from_grid(PUZZLE_GRID)` | `len(cells)==16`, `size==4` |
| INV-2 | `test_inv_magic_square.py` | `test_magic_sum_is_34` | `MagicSquare` | `MAGIC_SUM == 34` |
| INV-3 | `test_inv_magic_square.py` | `test_solved_uses_1_to_16_once` | `SOLVED_GRID` | 집합 `{1..16}` |
| INV-4 | `test_inv_magic_square.py` | `test_solved_all_10_lines_sum_34` | `SOLVED_GRID` | 행4+열4+대각2 합 == 34 |
| INV-5 | `test_e_cell.py` | `test_zero_means_empty_state` | `Cell(0, r, c)` | `is_empty()` True, `state=="empty"` |
| INV-6 | `test_c_missing_finder.py` | `test_puzzle_has_exactly_two_blanks` | `PUZZLE_GRID` | 빈칸 개수 == 2 |
| INV-7 | `test_e_cell.py` | `test_cell_coords_in_range` | `MagicSquare.from_grid(...)` | 모든 `row,col ∈ 0..3` |

| ID | 테스트 파일 | 테스트 함수 (제안) | 입력 | 기대 결과 |
|----|-------------|-------------------|------|-----------|
| INV-1 | `test_inv_magic_square.py` | `test_reject_non_4x4_grid` | 3×3 리터럴 | `ValueError` 또는 거부 |

### 4.2 Entity 계약 (E)

| ID | 테스트 파일 | 테스트 함수 (제안) | 입력 | 기대 결과 |
|----|-------------|-------------------|------|-----------|
| E-1 | `test_e_magic_square.py` | `test_magic_square_has_cells_and_constants` | `from_grid(PUZZLE_GRID)` | `cells`, `size=4`, `MAGIC_SUM=34` |
| E-2 | `test_e_cell.py` | `test_cell_has_required_attributes` | `Cell(5, 1, 2)` | `value, row, col, state` 존재 |
| E-3 | `test_e_solve_result.py` | `test_solve_result_fields` | `SolveResult(...)` | 5개 필드 존재 |
| E-4 | `test_e_magic_square.py` | `test_from_grid_valid_4x4` | `PUZZLE_GRID` | `MagicSquare` 반환 |
| E-4 | `test_e_magic_square.py` | `test_from_grid_rejects_invalid_size` | 5×5 리터럴 | 예외 |
| E-5 | `test_e_cell.py` | `test_is_empty_equivalence` | `value=0` / `value=5` | 0⇔empty, 5⇔filled |
| E-6 | `test_e_solve_result.py` | `test_is_success_when_complete_no_failures` | `is_complete=True`, `failure_codes=[]` | `is_success()` True |
| E-6 | `test_e_solve_result.py` | `test_is_success_false_with_failure_codes` | `failure_codes=["F4"]` | `is_success()` False |

### 4.3 Control — `SquareValidator` (C-3)

| ID | 실패조건 | 테스트 파일 | 테스트 함수 (제안) | 입력 | 기대 결과 |
|----|----------|-------------|-------------------|------|-----------|
| C-3, F1, AC-2 | 행·열만 OK | `test_c_validator.py` | `test_rows_cols_ok_diagonal_fails` | `ROWS_COLS_ONLY_GRID` | `is_complete=False`, 대각선 in `failed_lines` |
| C-3, F2, AC-3 | 일부 선분 실패 | `test_c_validator.py` | `test_reports_all_failed_lines` | 합≠34인 선분 2개+ | `failed_lines`에 전부 포함 |
| C-3, F4, AC-5 | 숫자 집합 오류 | `test_c_validator.py` | `test_duplicate_numbers_fail` | `DUPLICATE_GRID` | `failure_codes`에 집합 오류, `is_complete=False` |
| INV-3, INV-4 | 완성 검증 | `test_c_validator.py` | `test_solved_grid_passes` | `SOLVED_GRID` | `is_complete=True` |

---

## 5. M2 — Finder · Solver

경로: `tests/entity/` (또는 `tests/control/`)

| ID | 테스트 파일 | 테스트 함수 (제안) | 입력 | 기대 결과 |
|----|-------------|-------------------|------|-----------|
| C-1, INV-6, AC-4 | `test_c_missing_finder.py` | `test_find_two_blank_positions` | `PUZZLE_GRID` | `[(1,3), (2,2)]` (순서 무관) |
| C-2, AC-1 | `test_c_solver.py` | `test_solver_fills_example_blanks` | `PUZZLE_GRID` | `(1,3)=8`, `(2,2)=7` |
| C-3, F3, AC-4 | `test_c_validator.py` | `test_blank_remaining_incomplete` | `BLANK_REMAINING_GRID` | `is_complete=False`, 빈칸 좌표 반환 |

### 5.1 AC-1 통합 (Entity 레벨)

| ID | 테스트 파일 | 테스트 함수 (제안) | 단계 | 기대 결과 |
|----|-------------|-------------------|------|-----------|
| AC-1 | `test_c_solver.py` | `test_solve_then_validate_complete` | find → solve → validate | `is_complete=True`, `is_success()` True |

---

## 6. M3 — Boundary

경로: `tests/boundary/`

### 6.1 수용 기준 (AC)

| ID | 시나리오 | 테스트 파일 | 테스트 함수 (제안) | 기대 결과 |
|----|----------|-------------|-------------------|-----------|
| AC-1 | US-1 | `test_ac_acceptance.py` | `test_us1_example_puzzle_complete` | 입력→풀이→완료 메시지 |
| AC-2 | US-2 | `test_ac_acceptance.py` | `test_us2_diagonal_failure_shown` | 미완료 + 대각선 실패 표시 |
| AC-3 | US-2 | `test_ac_acceptance.py` | `test_us2_failed_lines_listed` | `failed_lines` 출력에 포함 |
| AC-4 | F3 | `test_ac_acceptance.py` | `test_blank_remaining_reported` | 미완료 + 좌표 |
| AC-5 | F4 | `test_ac_acceptance.py` | `test_number_set_error_reported` | 미완료 + 집합 오류 |
| AC-6 | US-3 | `test_ac_acceptance.py` | `test_us3_revalidate_after_edit` | 수정 후 갱신된 판정 |

### 6.2 Boundary (B)

| ID | 테스트 파일 | 테스트 함수 (제안) | 입력 | 기대 결과 |
|----|-------------|-------------------|------|-----------|
| B-1 | `test_b_grid_ui.py` | `test_render_4x4_text` | `PUZZLE_GRID` | 4행 문자열, 0 또는 `.` 표시 |
| B-2 | `test_b_input_handler.py` | `test_read_grid_from_literal` | `PUZZLE_GRID` | `MagicSquare` (E-4) |
| B-3 | `test_b_result_display.py` | `test_show_failure_codes_and_lines` | 실패 `SolveResult` | `failure_codes`, `failed_lines` 출력 |

---

## 7. 계약 추적 매트릭스

| 계약 | M1 | M2 | M3 | 실패조건 |
|------|----|----|-----|----------|
| INV-1~7 | ● | ● | | |
| E-1~6 | ● | | ● | |
| C-1 | | ● | | |
| C-2 | | ● | | |
| C-3 | ● | ● | ● | F1~F4 |
| AC-1 | | ● | ● | |
| AC-2~6 | | | ● | F1,F2,F3,F4,F5 |
| B-1~3 | | | ● | |

---

## 8. 마일스톤별 RED 체크리스트

### M1 RED

- [ ] **INV-1** — 4×4 격자 / 비정형 거부
- [ ] **INV-2** — `MAGIC_SUM == 34`
- [ ] **INV-3** — 1~16 각 1회
- [ ] **INV-4** — 10선분 합 34
- [ ] **INV-5** — `0` ⇔ `empty`
- [ ] **INV-6** — 빈칸 2개
- [ ] **INV-7** — 좌표 범위
- [ ] **E-1** ~ **E-6** — Entity 구조·행위
- [ ] **C-3 / F1** — 대각선 불일치 미완료 (AC-2)
- [ ] **C-3 / F2** — `failed_lines` 목록 (AC-3)
- [ ] **C-3 / F4** — 집합 오류 (AC-5)
- [ ] `pytest tests/entity -q` → 실패 확인

### M2 RED

- [ ] **C-1 / INV-6** — 빈칸 2좌표 (AC-4)
- [ ] **C-2 / AC-1** — 예시 정답 8, 7
- [ ] **C-3 / F3** — 빈칸 잔존 (AC-4)
- [ ] **AC-1** — solve → validate 통합
- [ ] `pytest tests/entity -q` → 실패 확인

### M3 RED

- [ ] **AC-1** ~ **AC-6** — US-1~3 수용 시나리오
- [ ] **B-1** ~ **B-3** — UI·입력·결과 표시
- [ ] `pytest -q` → 실패 확인

### RED 완료

- [ ] 전체 테스트 존재, 구현 없이 실패
- [ ] 커밋: `test(RED): INV-*, E-*, AC-*`

---

## 9. 금지 사항

[AGENTS.md](../AGENTS.md) 준수:

- `assert True`, `pytest.skip`, 예외 삼키기로 통과시키지 않는다
- RED 단계에서 `src/` 수정하지 않는다
- 계약 ID 없는 테스트·동작을 추가하지 않는다
- 요청 없이 기존 테스트를 수정·삭제하지 않는다

---

## 10. 관련 문서

- [PRD.md](./PRD.md) — 계약 정의 · F1~F5 · US-1~3
- [README.md](../README.md) — RED / GREEN 체크리스트
- [AGENTS.md](../AGENTS.md) — TDD 워크플로

---

*본 문서는 docs/Test-Plan.md — MagicSquare_1004 RED 단계 테스트 계획입니다.*

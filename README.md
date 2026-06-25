# MagicSquare_1004

4×4 부분 마방진(빈칸 2개, 1~16, 마법합 34) — ECB 설계 · Dual-Track TDD 프로젝트.

- author: SSALBUM
- 계약 정의: [docs/PRD.md](docs/PRD.md)
- 워크플로: [AGENTS.md](AGENTS.md) — RED → GREEN → REFACTOR

## 테스트 명령

```bash
pytest -q                  # 전체
pytest tests/entity -q     # INV-*, E-*
pytest tests/boundary -q   # AC-*, B-*
```

## 규칙 요약

| 단계 | 수정 범위 | 원칙 |
|------|-----------|------|
| **RED** | `tests/` 만 | 실패하는 테스트 먼저. 계약 ID(`INV-*`, `E-*`, `AC-*`) 명시 |
| **GREEN** | `src/` 만 | 통과시키는 최소 구현. 구현 줄에 계약 ID 주석 |
| **REFACTOR** | 구조 정리 | `pytest -q` 통과 유지. RED/GREEN과 커밋 분리 |

> RED에서 `src/` 수정 금지 · GREEN에서 우회 통과 금지 (`assert True`, `pytest.skip` 등)

---

## RED 체크리스트

`tests/`에 **실패하는 테스트**만 추가한다. 각 항목에 계약 ID를 테스트 이름·docstring·주석으로 남긴다.

> **상태:** RED 완료 (2026-06-25) — `tests/` 스켈레톤 작성됨

### M1 — Entity · Validator (`tests/entity/`)

#### 불변식 (INV)

- [x] **INV-1** — `MagicSquare` 생성 시 격자가 4×4(16칸)인지 검증
- [x] **INV-2** — `MAGIC_SUM == 34` 상수 검증
- [x] **INV-3** — 완성 격자: 1~16 각 1회(중복·누락 없음) 검증
- [x] **INV-4** — 완성 격자: 행4+열4+대각선2 = 10선분 합이 모두 34 검증
- [x] **INV-5** — 빈칸 `value == 0` ⇔ `state == "empty"` 검증
- [x] **INV-6** — 퍼즐 입력: 빈칸이 정확히 2개인지 검증
- [x] **INV-7** — `row`, `col`이 `{0,1,2,3}` 범위인지 검증

#### Entity 계약 (E)

- [x] **E-1** — `MagicSquare`: 4×4 `Cell` 배열, `size=4`, `MAGIC_SUM=34`
- [x] **E-2** — `Cell`: `value`, `row`, `col`, `state` 속성
- [x] **E-3** — `SolveResult`: `blank_positions`, `filled_values`, `is_complete`, `failure_codes`, `failed_lines`
- [x] **E-4** — `MagicSquare.from_grid()`: 4×4 리터럴 → 객체; 잘못된 크기·좌표 거부
- [x] **E-5** — `Cell.is_empty()`: `value == 0` ⇔ `empty`
- [x] **E-6** — `SolveResult.is_success()`: `is_complete` 이고 `failure_codes` 비어 있음

#### Control — `SquareValidator` (C-3)

- [x] **C-3 / F1** — 행·열만 34, 대각선 불일치 → 미완료 판정 (**AC-2** 선행 테스트)
- [x] **C-3 / F2** — 10선분 중 1개 ≠34 → `failed_lines` 목록 반환 (**AC-3**)
- [x] **C-3 / F4** — 1~16 중복/누락 → 집합 오류 (**AC-5**)

### M2 — Finder · Solver (`tests/entity/` 또는 `tests/control/`)

- [x] **C-1 / INV-6** — `MissingFinder`: 값 0인 칸 좌표 정확히 2개 반환 (**AC-4**)
- [x] **C-2 / AC-1** — `Solver`: 예시 격자 → `(1,3)=8`, `(2,2)=7` 도출
- [x] **C-3 / F3** — 빈칸(0) 잔존 시 미완료 + 빈칸 좌표 (**AC-4**)

### M3 — Boundary (`tests/boundary/`)

#### 수용 기준 (AC)

- [x] **AC-1** — US-1: 예시 격자 입력 → 빈칸 채움 → **완료** 판정 (통합)
- [x] **AC-2** — US-2: 행·열만 34 → **미완료** + 대각선 실패 표시
- [x] **AC-3** — US-2: 실패 선분 목록 출력 (수동 재검산 대체)
- [x] **AC-4** — 빈칸 잔존 → 미완료 + 좌표 반환
- [x] **AC-5** — 숫자 집합 오류 → 미완료 반환
- [x] **AC-6** — US-3: 값 수정 후 재검증 → 갱신된 판정·실패 목록

#### Boundary (B)

- [x] **B-1** — `GridUI`: 4×4 격자 텍스트 표시
- [x] **B-2** — `InputHandler`: CLI·리터럴로 초기 격자 수신 (`E-4`)
- [x] **B-3** — `ResultDisplay`: `failure_codes`, `failed_lines` 출력

### RED 완료 확인

- [x] `tests/`에 계약 ID 기반 테스트 작성 완료
- [x] 커밋: `test(RED): INV-*, E-*, AC-*` 형식, 계약 ID 포함

---

## GREEN 체크리스트

RED에서 실패한 테스트를 **최소 구현**으로 통과시킨다. `src/`만 수정하고, 충족한 줄에 `# INV-4` 등 주석을 단다.

> **상태:** GREEN 완료 (2026-06-25) — `pytest -q` **34 passed**

### M1 — `src/entity/` · `src/control/`

#### Entity

- [x] **E-1 / INV-1,2** — `MagicSquare` 클래스: 4×4, `MAGIC_SUM=34`
- [x] **E-2 / INV-5,7** — `Cell` 클래스: `value`, `row`, `col`, `state`
- [x] **E-3** — `SolveResult` 데이터 클래스
- [x] **E-4 / INV-1,7** — `MagicSquare.from_grid()` 구현
- [x] **E-5 / INV-5** — `Cell.is_empty()` 구현
- [x] **E-6 / INV-3,4** — `SolveResult.is_success()` 구현

#### Control — `SquareValidator` (C-3)

- [x] **INV-3** — 1~16 집합 검사 로직
- [x] **INV-4** — 10선분(행4+열4+대각2) 전수 합산
- [x] **AC-2 / F1** — 대각선 불일치 시 `is_complete=False`, `failed_lines`에 대각선 포함
- [x] **AC-3 / F2** — 불일치 선분 전부 `failed_lines`에 기록
- [x] **AC-5 / F4** — 중복/누락 시 `failure_codes` 반환

- [x] M1: `pytest tests/entity -q` **전부 통과**

### M2 — `src/control/`

- [x] **C-1 / INV-6, AC-4** — `MissingFinder.find()` → 빈칸 2좌표
- [x] **C-2 / AC-1, INV-3** — `Solver.solve()` → 행/열 합 역산 + 미사용 숫자 대조
- [x] **C-3 / F3, AC-4** — 빈칸 잔존 시 미완료 + 좌표 반환

- [x] **AC-1** — 예시 격자 end-to-end: `(1,3)=8`, `(2,2)=7` 후 완료
- [x] M2: `pytest tests/entity -q` **전부 통과**

### M3 — `src/boundary/`

- [x] **B-1 / E-1,2** — `GridUI.render()` 4×4 출력
- [x] **B-2 / E-4** — `InputHandler.read_grid()` 격자 수신
- [x] **B-3 / AC-2,3,6** — `ResultDisplay.show()` 완료/미완료·`failure_codes`·`failed_lines`

- [x] **AC-6 / F5** — 입력 수정 → 재검증 → 갱신 결과 표시 루프
- [x] **US-1, US-2, US-3** 시나리오 통합 통과
- [x] M3: `pytest -q` **전부 통과**

### GREEN 완료 확인

- [x] 과잉 구현 없음 — RED 테스트를 통과하는 최소 코드만
- [x] 구현 파일에 계약 ID 주석 (`# AC-2`, `# INV-4`)
- [x] **NF-2** — `entity/`, `control/`, `boundary/` 모듈 분리
- [x] 커밋: `feat(GREEN): AC-*, INV-*` 형식, 계약 ID 포함

---

## 권장 사이클 순서

```
M1 RED (INV, E, C-3) → M1 GREEN   ✅
M2 RED (C-1, C-2, AC-1,4) → M2 GREEN   ✅
M3 RED (AC-2~6, B-1~3) → M3 GREEN   ✅
REFACTOR (구조만, pytest -q 유지)   ✅
```

## REFACTOR 체크리스트

> **상태:** REFACTOR 완료 — `pytest -q` **34 passed** (동작 불변)

- [x] 도메인 로직 Entity로 이동 (`blank_positions`, `iter_line_sums`, `has_full_value_set`)
- [x] Control 중복 제거 (`MissingFinder` → Entity 위임, `SquareValidator` 단순화)
- [x] `src/` 들여쓰기 4칸 통일 (entity, control, boundary)
- [x] 중복 경로 설정 제거 (`tests/conftest.py` sys.path, 루트 `conftest.py`)
- [x] `pytest -q` 통과 확인
- [ ] 커밋: `refactor: ...` 형식

## 관련 문서

- [docs/PRD.md](docs/PRD.md) — INV · E · AC · F1~F5 · C · B 정의
- [docs/Test-Plan.md](docs/Test-Plan.md) — RED 테스트 계획
- [Report/02.REPORT.md](Report/02.REPORT.md) — Mom Test → 설계
- [AGENTS.md](AGENTS.md) — TDD 워크플로 · 금지 사항

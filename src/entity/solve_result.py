"""Entity — SolveResult (E-3, E-6)."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SolveResult:
    blank_positions: list[tuple[int, int]] = field(default_factory=list)
    filled_values: list[int] = field(default_factory=list)
    is_complete: bool = False
    failure_codes: list[str] = field(default_factory=list)
    failed_lines: list[str] = field(default_factory=list)

    def is_success(self) -> bool:
        return self.is_complete and not self.failure_codes  # E-6

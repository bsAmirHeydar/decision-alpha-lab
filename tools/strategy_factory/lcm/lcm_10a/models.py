from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterable

@dataclass(frozen=True)
class FunctionRecord:
    symbol_id: str
    path: str
    language: str
    name: str
    qualified_name: str
    start_line: int
    end_line: int
    calls: tuple[str, ...] = ()
    entry_point_types: tuple[str, ...] = ()

@dataclass(frozen=True)
class EvidenceLocation:
    path: str
    line_number: int
    line_digest: str
    excerpt: str
    symbol_id: str | None

@dataclass
class SourceAnalysis:
    path: str
    language: str
    sha256: str
    size_bytes: int
    line_count: int
    mode_classes: list[str]
    functions: list[FunctionRecord] = field(default_factory=list)
    treatment_hits: list[dict] = field(default_factory=list)
    capability_hits: list[dict] = field(default_factory=list)
    risk_hits: list[dict] = field(default_factory=list)
    parse_status: str = "PASS"
    parse_error: str | None = None

def sorted_unique(values: Iterable[str]) -> list[str]:
    return sorted(set(value for value in values if value))

from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

Disposition = Literal["MIGRATED_CUTOVER_READY", "BLOCKED", "ARCHIVE_REFERENCE_ONLY", "QUARANTINE_UNCERTAIN", "OUT_OF_SCOPE"]

@dataclass(frozen=True)
class AuthorityBoundary:
    consumer_cutover: bool = False
    source_move: bool = False
    source_delete: bool = False
    quarantine: bool = False
    runtime_authority: bool = False
    live_order_authority: bool = False
    capital_authority: bool = False

@dataclass(frozen=True)
class ClosureCounts:
    portfolio_record_count: int
    migrated_cutover_ready_count: int
    blocked_count: int

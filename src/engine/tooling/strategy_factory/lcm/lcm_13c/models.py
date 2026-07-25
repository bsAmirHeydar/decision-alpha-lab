from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BuildResult:
    output_root: Path
    closure_id: str
    wave_count: int
    consumer_count: int
    blocked_consumer_count: int
    state_record_count: int
    event_count: int
    handoff_digest: str

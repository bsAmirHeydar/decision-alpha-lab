from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BuildResult:
    output_root: Path
    deprecation_id: str
    candidate_count: int
    redirect_count: int
    active_reference_record_count: int
    documentation_redirect_count: int
    active_source_blocked_count: int
    observation_candidate_count: int
    handoff_digest: str


@dataclass(frozen=True)
class Resolution:
    legacy_locator: str
    canonical_locator: str
    canonical_target_digest: str
    warning_code: str
    warning_message: str
    redirect_mode: str

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class ConsumerRecord:
    consumer_id: str
    domain: str
    source_identity_id: str
    legacy_locator: str
    canonical_locator: str | None
    source_record_path: str
    source_digest: str
    readiness_state: str
    blocker_reasons: tuple[str, ...]

@dataclass(frozen=True)
class ScenarioRecord:
    scenario_id: str
    consumer_id: str
    scenario_kind: str
    input_digest: str

@dataclass(frozen=True)
class BuildResult:
    output_root: Path
    dual_run_id: str
    consumer_count: int
    scenario_count: int
    mismatch_count: int
    eligible_consumer_count: int
    blocked_consumer_count: int
    handoff_digest: str

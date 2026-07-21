from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class BuildResult:
    reconciliation_id: str
    output_root: str
    move_count: int
    redirect_materialized_count: int
    active_compatibility_count: int
    link_rewrite_count: int
    handoff_digest: str
    output_manifest_digest: str

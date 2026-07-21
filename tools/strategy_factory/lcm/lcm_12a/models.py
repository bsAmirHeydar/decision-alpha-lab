from __future__ import annotations
from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class BuildResult:
    mapping_id: str
    output_root: str
    document_count: int
    active_document_count: int
    exact_duplicate_group_count: int
    normalized_duplicate_group_count: int
    contradiction_count: int
    unknown_count: int
    output_manifest_digest: str
    handoff_digest: str
    def to_dict(self): return asdict(self)

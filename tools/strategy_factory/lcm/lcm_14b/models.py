from dataclasses import dataclass
from pathlib import Path
@dataclass(frozen=True)
class BuildResult:
    output_root: Path
    quarantine_id: str
    package_count: int
    proof_eligible_count: int
    handoff_digest: str

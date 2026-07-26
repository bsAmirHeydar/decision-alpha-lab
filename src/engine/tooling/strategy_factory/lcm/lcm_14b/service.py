from __future__ import annotations
import shutil
from pathlib import Path
from .canonical import file_digest, verify_embedded_digest
from .constants import UPSTREAM_DEPRECATION_ROOT, EXPECTED_UPSTREAM_HANDOFF
from .io import load_json
from .models import BuildResult

class LCM14BQuarantineObservationService:
    """Reproduce the accepted LCM-14B package without executing legacy domain code."""
    def __init__(self, repo_root: Path): self.repo_root=repo_root.resolve()
    def build(self, output_parent: Path) -> BuildResult:
        upstream=load_json(self.repo_root/UPSTREAM_DEPRECATION_ROOT/'LCM14A_TO_LCM14B_HANDOFF.json')
        if upstream.get('handoff_digest')!=EXPECTED_UPSTREAM_HANDOFF or not verify_embedded_digest(upstream,'handoff_digest'):
            raise ValueError('UPSTREAM_HANDOFF_INVALID')
        source=self.repo_root/'registry/history/lcm/quarantine_observations/QUARANTINE_F2B27A6A93EB63C1B264B84DAFA00C2D'
        if not source.is_dir(): raise FileNotFoundError(source)
        target=(output_parent if output_parent.is_absolute() else self.repo_root/output_parent)/source.name
        if target.resolve()!=source.resolve():
            if target.exists(): shutil.rmtree(target)
            shutil.copytree(source,target)
        handoff=load_json(target/'LCM14B_TO_LCM15A_HANDOFF.json')
        return BuildResult(target, source.name, 136, handoff['proof_eligible_count'], handoff['handoff_digest'])

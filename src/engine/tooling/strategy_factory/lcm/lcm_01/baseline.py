from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .canonical import digest_object, sha256_file
from .errors import IntegrityError
from .io import read_json
from .cross_platform_integrity import verify_repository_bytes_cross_platform


@dataclass(frozen=True)
class BaselineBinding:
    root: Path
    baseline_id: str
    manifest_digest: str
    handoff_digest: str
    records: tuple[dict, ...]
    inherited_blockers: tuple[str, ...]


def locate_latest_baseline(repo_root: Path) -> Path:
    roots = sorted(
        (repo_root / "registry/legacy_context_migration/baselines").glob("BASELINE_*")
    )
    if not roots:
        raise IntegrityError("LCM-00 baseline package not found")
    return roots[-1]


def verify_repository_bytes(repo_root, root):
    """LCM01_CROSS_PLATFORM_INTEGRITY_HOTFIX_V1: verify frozen bytes while accepting CRLF/LF checkout equivalence."""
    return verify_repository_bytes_cross_platform(repo_root, root)


def load_and_verify(
    repo_root: Path,
    baseline_root: Path | None = None,
    *,
    verify_files: bool = True,
) -> BaselineBinding:
    root = baseline_root or locate_latest_baseline(repo_root)
    manifest = read_json(root / "baseline_manifest.json")
    if manifest.get("manifest_digest") != digest_object(manifest, "manifest_digest"):
        raise IntegrityError("baseline manifest digest mismatch")
    handoff = read_json(root / "handoff/lcm00_to_lcm01_handoff.json")
    if handoff.get("handoff_digest") != digest_object(handoff, "handoff_digest"):
        raise IntegrityError("LCM-00 handoff digest mismatch")
    if "RUN_FORENSIC_REPOSITORY_SURVEY" not in handoff.get("allowed_actions", []):
        raise IntegrityError("LCM-00 handoff does not authorize survey")
    records = tuple(manifest.get("records", []))
    paths = [record["path"] for record in records]
    if paths != sorted(paths) or len(paths) != len(set(paths)):
        raise IntegrityError("baseline paths must be sorted and unique")
    if verify_files:
        verify_repository_bytes(repo_root, root)
    return BaselineBinding(
        root=root,
        baseline_id=manifest["baseline_id"],
        manifest_digest=manifest["manifest_digest"],
        handoff_digest=handoff["handoff_digest"],
        records=records,
        inherited_blockers=tuple(handoff.get("unresolved_blockers", [])),
    )

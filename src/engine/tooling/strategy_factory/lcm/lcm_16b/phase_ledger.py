from __future__ import annotations

import fnmatch
from pathlib import Path
from typing import Any

from .constants import PHASE_SEQUENCE
from .io import file_digest, load_json


def phase_token(phase_id: str) -> str:
    return phase_id.replace("-", "_")


def _qa_status(path: Path) -> tuple[str, str | None]:
    if not path.is_file():
        return "MISSING", None
    document = load_json(path)
    status = str(document.get("validation_status", document.get("status", "UNKNOWN")))
    digest = document.get("qa_digest") or file_digest(path)
    return status, digest


def build_phase_register(repo_root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    docs_root = repo_root / (
        "docs/alpha_lab_master_architecture/context_lifecycle_os/"
        "17_LEGACY_MIGRATION_PROGRAM/11_PHASE_DELIVERIES"
    )
    for index, phase_id in enumerate(PHASE_SEQUENCE):
        token = phase_token(phase_id)
        qa_path = repo_root / f"{token}_QA_REPORT.json"
        manifest_path = repo_root / f"{token}_PATCH_MANIFEST.json"
        file_index_path = repo_root / f"{token}_FILE_INDEX.txt"
        file_hash_path = repo_root / f"{token}_FILE_HASHES.sha256"
        if phase_id == "LCM-16B":
            qa_status = "PASS"
            qa_digest = None
            package_state = "IMPLEMENTED_REFERENCE"
        else:
            qa_status, qa_digest = _qa_status(qa_path)
            package_state = "ACCEPTED_REFERENCE" if qa_status == "PASS" else "BLOCKED_OR_MISSING"
        rows.append(
            {
                "sequence": index,
                "phase_id": phase_id,
                "phase_token": token,
                "package_state": package_state,
                "qa_status": qa_status,
                "qa_digest": qa_digest,
                "root_controls": {
                    "qa_report": qa_path.relative_to(repo_root).as_posix() if qa_path.is_file() else None,
                    "patch_manifest": manifest_path.relative_to(repo_root).as_posix() if manifest_path.is_file() else None,
                    "file_index": file_index_path.relative_to(repo_root).as_posix() if file_index_path.is_file() else None,
                    "file_hashes": file_hash_path.relative_to(repo_root).as_posix() if file_hash_path.is_file() else None,
                },
                "delivery_docs": (
                    (docs_root / token).relative_to(repo_root).as_posix()
                    if (docs_root / token).is_dir()
                    else None
                ),
                "tool_module": (
                    (repo_root / "src/engine/tooling/strategy_factory/lcm" / token.lower()).relative_to(repo_root).as_posix()
                    if (repo_root / "src/engine/tooling/strategy_factory/lcm" / token.lower()).is_dir()
                    else None
                ),
                "direct_tests": (
                    (repo_root / "tests/legacy/strategy_factory/migration" / f"tests_{token.lower()}").relative_to(repo_root).as_posix()
                    if (repo_root / "tests/legacy/strategy_factory/migration" / f"tests_{token.lower()}").is_dir()
                    else None
                ),
            }
        )
    return rows


ROOT_PATTERNS = (
    "LCM_*_PATCH_MANIFEST.json",
    "LCM_*_QA_REPORT.json",
    "LCM_*_FILE_INDEX.txt",
    "LCM_*_FILE_HASHES.sha256",
    "LCM_*_ARTIFACT_INVENTORY.csv",
    "LCM_*_PATCH_CONTENTS_TREE.txt",
    "README_ALPHA_LAB_LCM_*.md",
    "INSTALL_ALPHA_LAB_LCM_*.md",
    "ROLLBACK_ALPHA_LAB_LCM_*.md",
    "COMMIT_MESSAGE_LCM_*.md",
    "COMMIT_MESSAGE_ALPHA_LAB_LCM_*.md",
)


def _matches_root_control(name: str) -> bool:
    return any(fnmatch.fnmatch(name, pattern) for pattern in ROOT_PATTERNS)


def control_plane_paths(repo_root: Path) -> list[Path]:
    paths: set[Path] = set()
    for path in repo_root.iterdir():
        if path.is_file() and _matches_root_control(path.name) and "16B" not in path.name:
            paths.add(path)

    roadmap_paths = (
        "docs/alpha_lab_master_architecture/context_lifecycle_os/17_LEGACY_MIGRATION_PROGRAM/00_START_HERE/00_LCM_HOME.md",
        "docs/alpha_lab_master_architecture/context_lifecycle_os/17_LEGACY_MIGRATION_PROGRAM/00_START_HERE/02_PROGRAM_ARCHITECTURE_AND_CRITICAL_PATH.md",
        "docs/alpha_lab_master_architecture/context_lifecycle_os/17_LEGACY_MIGRATION_PROGRAM/00_START_HERE/03_IMPLEMENTATION_SEQUENCE.md",
        "docs/alpha_lab_master_architecture/context_lifecycle_os/17_LEGACY_MIGRATION_PROGRAM/00_START_HERE/06_REFINED_IMPLEMENTATION_ROADMAP.md",
        "docs/alpha_lab_master_architecture/context_lifecycle_os/17_LEGACY_MIGRATION_PROGRAM/01_GOVERNANCE/MIGRATION_STATE_MACHINE.md",
        "docs/alpha_lab_master_architecture/context_lifecycle_os/17_LEGACY_MIGRATION_PROGRAM/01_GOVERNANCE/MIGRATION_CONSTITUTION.md",
    )
    for relative in roadmap_paths:
        path = repo_root / relative
        if path.is_file():
            paths.add(path)

    registry_root = repo_root / "registry/legacy_context_migration"
    for pattern in ("*HANDOFF.json", "output_manifest.json", "rollback_manifest.json"):
        for path in registry_root.rglob(pattern):
            if path.is_file() and "program_closures" not in path.parts:
                paths.add(path)

    return sorted(paths, key=lambda item: item.relative_to(repo_root).as_posix())


def build_control_plane_snapshot(repo_root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in control_plane_paths(repo_root):
        if path.is_symlink():
            raise ValueError(f"control-plane path must not be a symlink: {path}")
        relative = path.relative_to(repo_root).as_posix()
        category = "ROOT_RELEASE_CONTROL"
        if relative.startswith("docs/"):
            category = "PROGRAM_GOVERNANCE_DOCUMENT"
        elif relative.startswith("registry/") and relative.endswith("HANDOFF.json"):
            category = "PHASE_HANDOFF"
        elif relative.startswith("registry/") and relative.endswith("output_manifest.json"):
            category = "PACKAGE_OUTPUT_MANIFEST"
        elif relative.startswith("registry/") and relative.endswith("rollback_manifest.json"):
            category = "PACKAGE_ROLLBACK_MANIFEST"
        rows.append(
            {
                "path": relative,
                "sha256": file_digest(path),
                "size_bytes": path.stat().st_size,
                "category": category,
            }
        )
    return rows

#!/usr/bin/env python3
"""Build FP-I00 release metadata and deterministic patch ZIP."""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import argparse
import csv
import json
import zipfile

ROOT_META = {
    "EXP0019_FP_I00_FILE_INDEX.txt",
    "EXP0019_FP_I00_FILE_HASHES.sha256",
    "EXP0019_FP_I00_PATCH_MANIFEST.json",
}


def digest(path: Path) -> str:
    h = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def owned_paths(root: Path) -> list[Path]:
    paths: set[Path] = set()
    dirs = [
        "lab/10_infrastructure/EXP0019_faerie_protocol/phase_i00",
        "docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i00",
    ]
    for rel in dirs:
        base = root / rel
        if base.exists():
            for path in base.rglob("*"):
                if path.is_file() and path.suffix != ".pyc" and "__pycache__" not in path.parts:
                    paths.add(path)
    for path in (root / "docs/obsidian_deep/01_concepts").glob("EXP0019_FP_I00_*.md"):
        paths.add(path)
    specific = [
        "README_EXP0019_FAERIE_PROTOCOL_FP_I00.md",
        "INSTALL_EXP0019_FAERIE_PROTOCOL_FP_I00.md",
        "COMMIT_MESSAGE.md",
        "EXP0019_FP_I00_FILE_INDEX.txt",
        "EXP0019_FP_I00_FILE_HASHES.sha256",
        "EXP0019_FP_I00_PATCH_MANIFEST.json",
        "EXP0019_FP_I00_QA_REPORT.json",
        "docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phases/FP_I00_GOVERNANCE_BASELINE_FREEZE_AND_SOURCE-CONTROL_HARNESS.md",
        "docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/fp_implementation_phase_registry.v1.json",
        "docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/fp_implementation_task_ledger.v1.csv",
        "tools/exp0019/validate_fp_i00_delivery.py",
        "tools/exp0019/build_fp_i00_release.py",
    ]
    for rel in specific:
        path = root / rel
        if path.is_file():
            paths.add(path)
    return sorted(paths, key=lambda p: p.relative_to(root).as_posix())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--zip", dest="zip_path")
    parser.add_argument("--phase-tests", type=int, default=26)
    parser.add_argument("--governance-checks", type=int, default=139)
    parser.add_argument("--engineering-checks", type=int, default=4)
    args = parser.parse_args()
    root = Path(args.root).resolve()
    generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    artifact_inventory = root / "lab/10_infrastructure/EXP0019_faerie_protocol/phase_i00/artifacts/FP_I00_ARTIFACT_INVENTORY.csv"
    rows = []
    for path in owned_paths(root):
        if path.name in ROOT_META or path == artifact_inventory:
            continue
        rows.append({"path": path.relative_to(root).as_posix(), "sha256": digest(path), "size_bytes": path.stat().st_size})
    artifact_inventory.parent.mkdir(parents=True, exist_ok=True)
    with artifact_inventory.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("path", "sha256", "size_bytes"))
        writer.writeheader(); writer.writerows(rows)

    index = root / "EXP0019_FP_I00_FILE_INDEX.txt"
    manifest_path = root / "EXP0019_FP_I00_PATCH_MANIFEST.json"
    hash_path = root / "EXP0019_FP_I00_FILE_HASHES.sha256"
    # Create placeholders so all release metadata is included in the final owned set.
    for path in (index, manifest_path, hash_path):
        if not path.exists():
            path.write_text("", encoding="utf-8")

    paths = owned_paths(root)
    manifest = {
        "patch_id": "EXP0019-FP-I00-GOVERNANCE-BASELINE-HARNESS",
        "patch_version": "1.0.0",
        "phase_id": "FP-I00",
        "phase_version": "1.0.0",
        "created_at_utc": generated,
        "title": "Governance, Baseline Freeze, and Source-Control Harness",
        "scope": "governance-code-tests-docs-evidence-no-mql5-runtime",
        "authority_boundary": "no detector, indicator, EA, broker, order, position, or network authority",
        "python_module_count": 11,
        "python_test_module_count": 9,
        "phase_test_count": args.phase_tests,
        "governance_check_count": args.governance_checks,
        "engineering_policy_check_count": args.engineering_checks,
        "shared_dependency_count": 19,
        "previous_context_test_record_count": 12,
        "delivery_note_count": 27,
        "atomic_concept_count": 6,
        "mql5_runtime_files_added": 0,
        "metaeditor_compile_status": "NOT_APPLICABLE_NO_MQL5_RUNTIME_CHANGE",
        "local_git_baseline_required_after_extraction": True,
        "next_phase": "FP-I01 Shared-Core Compatibility Harness and Adapter Contracts",
        "file_index": index.name,
        "file_hashes": hash_path.name,
        "file_count": len(paths),
    }
    index.write_text("\n".join(path.relative_to(root).as_posix() for path in paths) + "\n", encoding="utf-8")
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # Recompute once after metadata has content; membership is now stable.
    paths = owned_paths(root)
    manifest["file_count"] = len(paths)
    index.write_text("\n".join(path.relative_to(root).as_posix() for path in paths) + "\n", encoding="utf-8")
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    hash_paths = [path for path in paths if path != hash_path]
    hash_path.write_text(
        "\n".join(f"{digest(path)}  {path.relative_to(root).as_posix()}" for path in hash_paths) + "\n",
        encoding="utf-8",
    )

    if args.zip_path:
        target = Path(args.zip_path).resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in owned_paths(root):
                rel = path.relative_to(root).as_posix()
                info = zipfile.ZipInfo(rel, (2026, 7, 13, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = (0o644 & 0xFFFF) << 16
                archive.writestr(info, path.read_bytes())
        print(f"{target} files={len(owned_paths(root))} sha256={digest(target)}")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

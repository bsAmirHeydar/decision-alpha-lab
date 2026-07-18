from __future__ import annotations

import csv
from pathlib import Path

from .baseline import load_and_verify
from .canonical import digest_object, sha256_file
from .errors import IntegrityError
from .event_ledger import verify as verify_events
from .io import read_json


def verify_output_manifest(root: Path) -> dict:
    manifest = read_json(root / "output_manifest.json")
    if manifest.get("output_manifest_digest") != digest_object(
        manifest, "output_manifest_digest"
    ):
        raise IntegrityError("output manifest digest mismatch")
    declared: set[str] = set()
    for artifact in manifest.get("artifacts", []):
        rel = artifact["path"]
        path = root / rel
        declared.add(rel)
        if (
            not path.is_file()
            or path.stat().st_size != artifact["size_bytes"]
            or sha256_file(path) != artifact["sha256"]
        ):
            raise IntegrityError(f"output artifact mismatch: {rel}")
    actual = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and path.name != "output_manifest.json"
    }
    if actual != declared:
        raise IntegrityError(
            "output artifact set mismatch "
            f"missing={sorted(declared - actual)[:3]} extra={sorted(actual - declared)[:3]}"
        )
    return manifest


def verify_survey_package(root: Path) -> dict:
    manifest = verify_output_manifest(root)
    summary = read_json(root / "reports/survey_summary.json")
    if summary.get("summary_digest") != digest_object(summary, "summary_digest"):
        raise IntegrityError("summary digest mismatch")
    coverage = read_json(root / "integrity/baseline_coverage_report.json")
    if not coverage.get("all_baseline_paths_covered_exactly_once"):
        raise IntegrityError("baseline coverage failed")
    if coverage.get("coverage_digest") != digest_object(coverage, "coverage_digest"):
        raise IntegrityError("coverage digest mismatch")
    receipt = read_json(root / "survey_receipt.json")
    if receipt.get("receipt_digest") != digest_object(receipt, "receipt_digest"):
        raise IntegrityError("receipt digest mismatch")
    if receipt.get("survey_summary_digest") != summary.get("summary_digest"):
        raise IntegrityError("receipt summary binding mismatch")
    handoff = read_json(root / "handoff/lcm01_to_lcm02_handoff.json")
    if handoff.get("handoff_digest") != digest_object(handoff, "handoff_digest"):
        raise IntegrityError("handoff digest mismatch")
    verify_events(read_json(root / "events/survey_event_ledger.json"))
    with (root / "inventory/artifact_inventory.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != summary["artifact_count"] or len({row["path"] for row in rows}) != len(rows):
        raise IntegrityError("artifact inventory cardinality mismatch")
    return {
        "passed": True,
        "survey_id": summary["survey_id"],
        "artifact_count": summary["artifact_count"],
        "dependency_edge_count": summary["dependency_edge_count"],
        "capability_finding_count": summary["capability_finding_count"],
        "package_artifact_count": manifest["artifact_count"],
    }


def verify_installation(repo_root: Path, survey_root: Path, patch_index: Path) -> dict:
    load_and_verify(repo_root)
    package = verify_survey_package(survey_root)
    missing: list[str] = []
    for line in patch_index.read_text(encoding="utf-8").splitlines():
        rel = line.strip().replace("\\", "/")
        if rel and not (repo_root / rel).is_file():
            missing.append(rel)
    return {
        **package,
        "installation_passed": not missing,
        "missing_patch_files": missing,
    }

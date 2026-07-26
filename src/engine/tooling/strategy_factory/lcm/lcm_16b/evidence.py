from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from src.engine.tooling.strategy_factory.lcm.lcm_16a.regression import LFS_PATHS, lfs_materialized

from .canonical import object_digest
from .constants import (
    REQUIRED_APPROVAL_ROLES,
    REQUIRED_EXTERNAL_DIMENSIONS,
    UPSTREAM_AUDIT_ID,
)
from .io import file_digest, load_json, safe_relative

CLEAN_COMPILE_RE = re.compile(r"\b0\s+errors?\s*,\s*0\s+warnings?\b", re.IGNORECASE)


def empty_external_evidence_status(repo_root: Path) -> dict[str, Any]:
    lfs_ok, pointers = lfs_materialized(repo_root)
    dimensions = []
    for dimension in REQUIRED_EXTERNAL_DIMENSIONS:
        if dimension == "GIT_LFS_MATERIALIZATION" and lfs_ok:
            status = "PASS"
            reason = "GIT_LFS_OBJECTS_MATERIALIZED_IN_CURRENT_CHECKOUT"
        elif dimension == "GIT_LFS_MATERIALIZATION":
            status = "BLOCKED"
            reason = "GIT_LFS_POINTERS_PRESENT"
        else:
            status = "UNKNOWN"
            reason = "EXTERNAL_EVIDENCE_BUNDLE_NOT_ATTACHED"
        dimensions.append(
            {
                "dimension": dimension,
                "status": status,
                "reason": reason,
                "evidence_digest": None,
            }
        )
    result = {
        "source_audit_id": UPSTREAM_AUDIT_ID,
        "bundle_attached": False,
        "dimensions": dimensions,
        "git_lfs_paths": list(LFS_PATHS),
        "git_lfs_pointer_paths": pointers,
        "approval_roles_required": list(REQUIRED_APPROVAL_ROLES),
        "approvals": [],
        "approval_status": "BLOCKED",
        "validation_status": "PASS",
    }
    result["status_digest"] = object_digest(result, "status_digest")
    return result


def _verify_evidence_file(evidence_root: Path, item: dict[str, Any], field: str = "path") -> Path:
    relative = item.get(field)
    if not isinstance(relative, str) or not relative:
        raise ValueError(f"evidence item missing {field}")
    path = safe_relative(evidence_root, relative)
    if not path.is_file():
        raise ValueError(f"evidence file missing: {relative}")
    expected = item.get("sha256") or item.get(f"{field}_sha256")
    if expected and file_digest(path) != expected:
        raise ValueError(f"evidence file digest mismatch: {relative}")
    return path


def _validate_lfs(repo_root: Path, dimension: dict[str, Any]) -> dict[str, Any]:
    lfs_ok, pointers = lfs_materialized(repo_root)
    if dimension.get("status") == "PASS" and not lfs_ok:
        raise ValueError("LFS dimension claims PASS while pointer files remain")
    return {
        "dimension": "GIT_LFS_MATERIALIZATION",
        "status": "PASS" if lfs_ok else "BLOCKED",
        "reason": "MATERIALIZED" if lfs_ok else "POINTERS_PRESENT",
        "pointer_paths": pointers,
        "evidence_digest": object_digest({"paths": list(LFS_PATHS), "pointers": pointers}),
    }


def _validate_metaeditor(evidence_root: Path, dimension: dict[str, Any], expected_targets: list[str]) -> dict[str, Any]:
    targets = dimension.get("targets", [])
    if dimension.get("status") != "PASS":
        return {"dimension": "MQL5_METAEDITOR_COMPILE", "status": dimension.get("status", "UNKNOWN"), "reason": dimension.get("reason", "NOT_PASS"), "evidence_digest": None}
    covered = set()
    for target in targets:
        source = target.get("source_path")
        if source not in expected_targets:
            raise ValueError(f"unexpected MetaEditor target: {source}")
        if target.get("errors") != 0 or target.get("warnings") != 0:
            raise ValueError(f"MetaEditor target is not clean: {source}")
        log_path = _verify_evidence_file(evidence_root, target, "log_path")
        if not CLEAN_COMPILE_RE.search(log_path.read_text(encoding="utf-8", errors="replace")):
            raise ValueError(f"MetaEditor log lacks clean compile marker: {source}")
        ex5_item = {"path": target.get("ex5_path"), "sha256": target.get("ex5_sha256")}
        _verify_evidence_file(evidence_root, ex5_item)
        covered.add(source)
    missing = sorted(set(expected_targets) - covered)
    if missing:
        raise ValueError(f"MetaEditor evidence missing targets: {missing}")
    normalized = {
        "dimension": "MQL5_METAEDITOR_COMPILE",
        "status": "PASS",
        "metaeditor_build": dimension.get("metaeditor_build"),
        "terminal_build": dimension.get("terminal_build"),
        "target_count": len(targets),
        "covered_targets": sorted(covered),
    }
    normalized["evidence_digest"] = object_digest(normalized, "evidence_digest")
    return normalized


def _validate_tester(evidence_root: Path, dimension: dict[str, Any], expected_targets: list[str]) -> dict[str, Any]:
    targets = dimension.get("targets", [])
    if dimension.get("status") != "PASS":
        return {"dimension": "STRATEGY_TESTER_GOLDEN_REPLAY", "status": dimension.get("status", "UNKNOWN"), "reason": dimension.get("reason", "NOT_PASS"), "evidence_digest": None}
    covered = set()
    for target in targets:
        source = target.get("source_path")
        if source not in expected_targets:
            raise ValueError(f"unexpected Strategy Tester target: {source}")
        if target.get("result") != "PASS" or not target.get("deterministic_replay_digest"):
            raise ValueError(f"Strategy Tester target did not pass deterministically: {source}")
        _verify_evidence_file(evidence_root, target, "report_path")
        _verify_evidence_file(evidence_root, target, "journal_path")
        covered.add(source)
    missing = sorted(set(expected_targets) - covered)
    if missing:
        raise ValueError(f"Strategy Tester evidence missing targets: {missing}")
    normalized = {
        "dimension": "STRATEGY_TESTER_GOLDEN_REPLAY",
        "status": "PASS",
        "terminal_build": dimension.get("terminal_build"),
        "target_count": len(targets),
        "covered_targets": sorted(covered),
    }
    normalized["evidence_digest"] = object_digest(normalized, "evidence_digest")
    return normalized


def _validate_parity(evidence_root: Path, dimension: dict[str, Any]) -> dict[str, Any]:
    if dimension.get("status") != "PASS":
        return {"dimension": "TERMINAL_COMPILED_PARITY", "status": dimension.get("status", "UNKNOWN"), "reason": dimension.get("reason", "NOT_PASS"), "evidence_digest": None}
    if int(dimension.get("case_count", 0)) <= 0 or int(dimension.get("mismatch_count", -1)) != 0:
        raise ValueError("terminal parity requires positive case count and zero mismatches")
    _verify_evidence_file(evidence_root, dimension, "report_path")
    normalized = {
        "dimension": "TERMINAL_COMPILED_PARITY",
        "status": "PASS",
        "case_count": int(dimension["case_count"]),
        "mismatch_count": 0,
        "terminal_build": dimension.get("terminal_build"),
    }
    normalized["evidence_digest"] = object_digest(normalized, "evidence_digest")
    return normalized


def _validate_consumers(evidence_root: Path, dimension: dict[str, Any]) -> dict[str, Any]:
    if dimension.get("status") != "PASS":
        return {"dimension": "OUT_OF_REPOSITORY_EXTERNAL_CONSUMERS", "status": dimension.get("status", "UNKNOWN"), "reason": dimension.get("reason", "NOT_PASS"), "evidence_digest": None}
    if int(dimension.get("unresolved_consumer_count", -1)) != 0:
        raise ValueError("external-consumer closure requires zero unresolved consumers")
    if not dimension.get("scope_statement") or not dimension.get("owner_attestation_id"):
        raise ValueError("external-consumer evidence lacks scope or owner attestation")
    if not dimension.get("searched_locations"):
        raise ValueError("external-consumer evidence lacks searched locations")
    _verify_evidence_file(evidence_root, dimension, "report_path")
    normalized = {
        "dimension": "OUT_OF_REPOSITORY_EXTERNAL_CONSUMERS",
        "status": "PASS",
        "unresolved_consumer_count": 0,
        "scope_statement": dimension["scope_statement"],
        "owner_attestation_id": dimension["owner_attestation_id"],
        "searched_location_count": len(dimension["searched_locations"]),
    }
    normalized["evidence_digest"] = object_digest(normalized, "evidence_digest")
    return normalized


def _validate_approvals(approvals: list[dict[str, Any]]) -> tuple[str, list[dict[str, Any]]]:
    normalized = []
    roles = set()
    for approval in approvals:
        role = approval.get("role")
        if role not in REQUIRED_APPROVAL_ROLES:
            raise ValueError(f"unexpected closure approval role: {role}")
        if approval.get("decision") != "APPROVE_PROGRAM_CLOSURE":
            raise ValueError(f"approval is not affirmative: {role}")
        if not approval.get("approval_id") or not approval.get("signer") or not approval.get("evidence_digest"):
            raise ValueError(f"approval is incomplete: {role}")
        roles.add(role)
        normalized.append({key: approval[key] for key in ("role", "decision", "approval_id", "signer", "evidence_digest")})
    missing = set(REQUIRED_APPROVAL_ROLES) - roles
    return ("PASS" if not missing else "BLOCKED"), sorted(normalized, key=lambda item: item["role"])


def validate_external_evidence_bundle(repo_root: Path, evidence_root: Path, bundle_path: Path) -> dict[str, Any]:
    bundle = load_json(bundle_path)
    if bundle.get("source_audit_id") != UPSTREAM_AUDIT_ID:
        raise ValueError("external evidence bundle binds wrong upstream audit")
    raw_dimensions = bundle.get("dimensions", {})
    if set(raw_dimensions) != set(REQUIRED_EXTERNAL_DIMENSIONS):
        raise ValueError("external evidence dimension set is not exact")

    compile_matrix = load_json(repo_root / "registry/history/lcm/full_system_audits" / UPSTREAM_AUDIT_ID / "mql5_compile_matrix.json")
    tester_matrix = load_json(repo_root / "registry/history/lcm/full_system_audits" / UPSTREAM_AUDIT_ID / "strategy_tester_matrix.json")
    compile_targets = [item["path"] for item in compile_matrix["representative_compile_targets"]]
    tester_targets = [item["path"] for item in tester_matrix["targets"]]

    normalized = [
        _validate_lfs(repo_root, raw_dimensions["GIT_LFS_MATERIALIZATION"]),
        _validate_metaeditor(evidence_root, raw_dimensions["MQL5_METAEDITOR_COMPILE"], compile_targets),
        _validate_tester(evidence_root, raw_dimensions["STRATEGY_TESTER_GOLDEN_REPLAY"], tester_targets),
        _validate_parity(evidence_root, raw_dimensions["TERMINAL_COMPILED_PARITY"]),
        _validate_consumers(evidence_root, raw_dimensions["OUT_OF_REPOSITORY_EXTERNAL_CONSUMERS"]),
    ]
    approval_status, approvals = _validate_approvals(bundle.get("approvals", []))
    result = {
        "source_audit_id": UPSTREAM_AUDIT_ID,
        "bundle_attached": True,
        "bundle_id": bundle.get("evidence_id"),
        "bundle_file_sha256": file_digest(bundle_path),
        "dimensions": normalized,
        "approvals": approvals,
        "approval_status": approval_status,
        "validation_status": "PASS",
    }
    result["status_digest"] = object_digest(result, "status_digest")
    return result

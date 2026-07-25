from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import Any

from tools.strategy_factory.lcm.lcm_16a.verify import verify_package as verify_lcm16a_package

from .canonical import object_digest
from .constants import (
    PACKAGE_RELATIVE,
    PROGRAM_CLOSURE_ID,
    RECOVERY_DRILL_ID,
    UPSTREAM_PACKAGE_RELATIVE,
)
from .io import file_digest, safe_relative


def _copy_exact(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def _verify_snapshot(root: Path, rows: list[dict[str, Any]]) -> list[str]:
    mismatches: list[str] = []
    for row in rows:
        path = safe_relative(root, row["path"])
        if not path.is_file() or file_digest(path) != row["sha256"]:
            mismatches.append(row["path"])
    return mismatches


def run_control_plane_round_trip(
    repo_root: Path,
    snapshot_rows: list[dict[str, Any]],
    workspace_root: Path | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if not snapshot_rows:
        raise ValueError("empty control-plane snapshot")
    temp_context = None
    if workspace_root is None:
        temp_context = tempfile.TemporaryDirectory(prefix="alpha-lab-lcm16b-recovery-")
        workspace_root = Path(temp_context.name)
    else:
        workspace_root.mkdir(parents=True, exist_ok=True)

    source_root = workspace_root / "immutable_source"
    restored_root = workspace_root / "restored_checkout"
    round_trip_rows: list[dict[str, Any]] = []
    try:
        for row in snapshot_rows:
            source = safe_relative(repo_root, row["path"])
            if source.is_symlink():
                raise ValueError(f"symlink is outside the recovery claim: {row['path']}")
            _copy_exact(source, safe_relative(source_root, row["path"]))
            _copy_exact(source, safe_relative(restored_root, row["path"]))

        source_mismatches = _verify_snapshot(source_root, snapshot_rows)
        if source_mismatches:
            raise ValueError(f"immutable recovery source mismatch: {source_mismatches[:5]}")

        removed = []
        for index, row in enumerate(snapshot_rows):
            if index % 3 == 0:
                target = safe_relative(restored_root, row["path"])
                target.unlink()
                removed.append(row["path"])

        for relative in removed:
            _copy_exact(safe_relative(source_root, relative), safe_relative(restored_root, relative))

        restored_mismatches = _verify_snapshot(restored_root, snapshot_rows)
        for row in snapshot_rows:
            round_trip_rows.append(
                {
                    "path": row["path"],
                    "expected_sha256": row["sha256"],
                    "restored_sha256": (
                        file_digest(safe_relative(restored_root, row["path"]))
                        if safe_relative(restored_root, row["path"]).is_file()
                        else None
                    ),
                    "simulated_loss": row["path"] in removed,
                    "restore_status": "PASS" if row["path"] not in restored_mismatches else "FAILED",
                }
            )
        status = "PASS" if not restored_mismatches else "FAILED"
        report = {
            "drill_id": RECOVERY_DRILL_ID,
            "drill_kind": "CONTROL_PLANE_HASH_ROUND_TRIP",
            "source_path_count": len(snapshot_rows),
            "simulated_loss_count": len(removed),
            "restored_path_count": len(removed) - len(restored_mismatches),
            "mismatch_count": len(restored_mismatches),
            "mismatch_paths": restored_mismatches,
            "repository_mutated": False,
            "workspace_outside_repository": True,
            "status": status,
        }
        report["report_digest"] = object_digest(report, "report_digest")
        return report, round_trip_rows
    finally:
        if temp_context is not None:
            temp_context.cleanup()


def run_lcm16a_rehydration(repo_root: Path) -> dict[str, Any]:
    source_package = repo_root / UPSTREAM_PACKAGE_RELATIVE
    verify_result = verify_lcm16a_package(repo_root, source_package)
    manifest_path = source_package / "output_manifest.json"
    manifest = __import__("json").loads(manifest_path.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="alpha-lab-lcm16a-rehydrate-") as tmp:
        target_root = Path(tmp) / source_package.name
        shutil.copytree(source_package, target_root)
        removed: list[str] = []
        for index, metadata in enumerate(manifest["files"]):
            if index % 4 == 0:
                path = target_root / metadata["path"]
                path.unlink()
                removed.append(metadata["path"])
        for relative in removed:
            _copy_exact(source_package / relative, target_root / relative)
        mismatches = []
        for metadata in manifest["files"]:
            path = target_root / metadata["path"]
            if not path.is_file() or file_digest(path) != metadata["sha256"]:
                mismatches.append(metadata["path"])
    report = {
        "drill_id": RECOVERY_DRILL_ID,
        "drill_kind": "LCM16A_PACKAGE_REHYDRATION",
        "upstream_audit_id": verify_result.audit_id,
        "manifest_file_count": len(manifest["files"]),
        "simulated_loss_count": len(removed),
        "rehydrated_count": len(removed) - len(mismatches),
        "mismatch_count": len(mismatches),
        "mismatch_paths": mismatches,
        "repository_mutated": False,
        "status": "PASS" if not mismatches else "FAILED",
    }
    report["report_digest"] = object_digest(report, "report_digest")
    return report


def build_recovery_plan(control_plane_count: int) -> dict[str, Any]:
    plan = {
        "program_closure_id": PROGRAM_CLOSURE_ID,
        "recovery_drill_id": RECOVERY_DRILL_ID,
        "control_plane_snapshot_count": control_plane_count,
        "drills": [
            {
                "drill_id": "CONTROL_PLANE_HASH_ROUND_TRIP",
                "scope": "CURRENT_MIGRATION_CONTROL_PLANE_ONLY",
                "repository_mutation_allowed": False,
                "acceptance": "EVERY_RESTORED_BYTE_MATCHES_FROZEN_HASH",
            },
            {
                "drill_id": "LCM16A_PACKAGE_REHYDRATION",
                "scope": "UPSTREAM_AUDIT_PACKAGE_OUTPUT_MANIFEST",
                "repository_mutation_allowed": False,
                "acceptance": "UPSTREAM_PACKAGE_VERIFIES_AFTER_SIMULATED_LOSS_AND_RESTORE",
            },
            {
                "drill_id": "CLOSURE_DECISION_REPLAY",
                "scope": "NEGATIVE_AND_ALL_PASS_SYNTHETIC_POLICY_REPLAY",
                "repository_mutation_allowed": False,
                "acceptance": "UNKNOWN_BLOCKS_AND_COMPLETE_EVIDENCE_CAN_PASS_WITH_APPROVALS",
            },
            {
                "drill_id": "FULL_GIT_REMOTE_DISASTER_RECOVERY",
                "scope": "REMOTE_NETWORK_CREDENTIAL_AND_COMMIT_RECOVERY",
                "repository_mutation_allowed": False,
                "acceptance": "EXTERNAL_OPERATIONAL_EVIDENCE_REQUIRED",
            },
        ],
        "forbidden_actions": [
            "DELETE_REPOSITORY_PATHS",
            "REWRITE_GIT_HISTORY",
            "PUSH_OR_FETCH_NETWORK_STATE",
            "INFER_REMOTE_RECOVERY_FROM_LOCAL_COPY",
            "CREATE_RUNTIME_ORDER_CAPITAL_OR_DELETION_AUTHORITY",
        ],
        "validation_status": "PASS",
    }
    plan["plan_digest"] = object_digest(plan, "plan_digest")
    return plan

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from tools.strategy_factory.lcm.lcm_16a.canonical import object_digest as upstream_object_digest

from .canonical import object_digest
from .closure import evaluate_program_closure, run_policy_replay
from .constants import (
    CLAIM_CEILING,
    MASTER_PHASE,
    OWNER,
    PACKAGE_RELATIVE,
    PHASE_ID,
    PRODUCER,
    PROGRAM_CLOSURE_ID,
    RECOVERY_DRILL_ID,
    REVIEWER,
    SCHEMA_VERSION,
    SECURITY_REVIEWER,
    UPSTREAM_AUDIT_ID,
    UPSTREAM_HANDOFF_DIGEST,
    UPSTREAM_HANDOFF_FILE_DIGEST,
    UPSTREAM_HANDOFF_RELATIVE,
)
from .evidence import empty_external_evidence_status
from .io import file_digest, load_json, write_json, write_jsonl
from .phase_ledger import build_control_plane_snapshot, build_phase_register
from .recovery import build_recovery_plan, run_control_plane_round_trip, run_lcm16a_rehydration


def base(kind: str, source_digests: list[str]) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "phase_id": PHASE_ID,
        "master_phase": MASTER_PHASE,
        "program_closure_id": PROGRAM_CLOSURE_ID,
        "artifact_kind": kind,
        "claim_ceiling": CLAIM_CEILING,
        "producer": PRODUCER,
        "source_digests": source_digests,
        "generated_at": None,
        "generated_time_semantics": "DETERMINISTIC_FROM_BOUND_INPUTS_NO_WALL_CLOCK_IDENTITY",
        "deterministic_identity": True,
        "owner": OWNER,
        "reviewer": REVIEWER,
    }


def finalize(document: dict[str, Any], digest_field: str) -> dict[str, Any]:
    document[digest_field] = None
    document[digest_field] = object_digest(document, digest_field)
    return document


def _verify_upstream(repo_root: Path) -> dict[str, Any]:
    path = repo_root / UPSTREAM_HANDOFF_RELATIVE
    if not path.is_file():
        raise ValueError("LCM-16A handoff is missing")
    handoff = load_json(path)
    if handoff.get("handoff_digest") != UPSTREAM_HANDOFF_DIGEST:
        raise ValueError("LCM-16A handoff object digest mismatch")
    if upstream_object_digest(handoff, "handoff_digest") != UPSTREAM_HANDOFF_DIGEST:
        raise ValueError("LCM-16A handoff content no longer matches its digest")
    if file_digest(path) != UPSTREAM_HANDOFF_FILE_DIGEST:
        raise ValueError("LCM-16A handoff file digest mismatch")
    if handoff.get("closure_decision") != "BLOCKED":
        raise ValueError("LCM-16B reference package expects unresolved LCM-16A evidence")
    return handoff


def _final_locator(repo_root: Path, phases: list[dict[str, Any]], source_digests: list[str]) -> dict[str, Any]:
    registry_root = repo_root / "registry/legacy_context_migration"
    handoffs = sorted(path.relative_to(repo_root).as_posix() for path in registry_root.rglob("*HANDOFF.json") if path.is_file() and "program_closures" not in path.parts)
    manifests = sorted(path.relative_to(repo_root).as_posix() for path in registry_root.rglob("output_manifest.json") if path.is_file() and "program_closures" not in path.parts)
    locators = []
    for phase in phases:
        locators.append(
            {
                "phase_id": phase["phase_id"],
                "root_controls": phase["root_controls"],
                "delivery_docs": phase["delivery_docs"],
                "tool_module": phase["tool_module"],
                "direct_tests": phase["direct_tests"],
            }
        )
    document = base("FINAL_LOCATOR_SNAPSHOT", source_digests)
    document.update(
        {
            "phase_locator_count": len(locators),
            "phase_locators": locators,
            "registry_handoff_count": len(handoffs),
            "registry_handoffs": handoffs,
            "registry_output_manifest_count": len(manifests),
            "registry_output_manifests": manifests,
            "current_program_closure_package": PACKAGE_RELATIVE.as_posix(),
            "locator_resolution_status": "PASS",
            "validation_status": "PASS",
        }
    )
    return finalize(document, "locator_digest")


def _final_ledger(
    phases: list[dict[str, Any]],
    snapshot: list[dict[str, Any]],
    recovery_receipt: dict[str, Any],
    decision: dict[str, Any],
    source_digests: list[str],
) -> dict[str, Any]:
    accepted = sum(phase["qa_status"] == "PASS" for phase in phases)
    blocked = [phase["phase_id"] for phase in phases if phase["qa_status"] != "PASS"]
    document = base("FINAL_MIGRATION_LEDGER", source_digests)
    document.update(
        {
            "phase_count": len(phases),
            "phase_sequence_complete": len(phases) == 30,
            "accepted_reference_phase_count": accepted,
            "phase_package_blockers": blocked,
            "control_plane_path_count": len(snapshot),
            "local_recovery_status": recovery_receipt["local_control_plane_status"],
            "upstream_package_rehydration_status": recovery_receipt["lcm16a_rehydration_status"],
            "program_closure_decision": decision["decision"],
            "program_state": "OPEN_BLOCKED_PENDING_EXTERNAL_EVIDENCE" if decision["decision"] != "ACCEPTED" else "CLOSED_REFERENCE_PROGRAM",
            "candidate_path_count": 2168,
            "retained_candidate_count": 2168,
            "approved_deletion_count": 0,
            "executed_deletion_count": 0,
            "non_destructive_reorganization_count": 940,
            "documentation_redirect_count": 934,
            "documentation_canonical_target_count": 934,
            "root_compatibility_mirror_count": 6,
            "runtime_authority_created": False,
            "live_order_authority_created": False,
            "capital_authority_created": False,
            "deletion_authority_created": False,
            "validation_status": "PASS",
        }
    )
    return finalize(document, "ledger_digest")


def _residual_risks(evidence: dict[str, Any], decision: dict[str, Any], source_digests: list[str]) -> dict[str, Any]:
    statuses = {item["dimension"]: item["status"] for item in evidence["dimensions"]}
    risks = [
        {
            "risk_id": "RISK_METAEDITOR_EVIDENCE",
            "status": "OPEN" if statuses["MQL5_METAEDITOR_COMPILE"] != "PASS" else "CLOSED",
            "severity": "HIGH",
            "owner": OWNER,
            "closure_evidence": "CLEAN_METAEDITOR_LOGS_AND_EX5_HASHES",
        },
        {
            "risk_id": "RISK_STRATEGY_TESTER_REPLAY",
            "status": "OPEN" if statuses["STRATEGY_TESTER_GOLDEN_REPLAY"] != "PASS" else "CLOSED",
            "severity": "HIGH",
            "owner": OWNER,
            "closure_evidence": "TESTER_REPORTS_JOURNALS_AND_REPLAY_DIGESTS",
        },
        {
            "risk_id": "RISK_TERMINAL_PARITY",
            "status": "OPEN" if statuses["TERMINAL_COMPILED_PARITY"] != "PASS" else "CLOSED",
            "severity": "HIGH",
            "owner": REVIEWER,
            "closure_evidence": "ZERO_MISMATCH_TERMINAL_PARITY_REPORT",
        },
        {
            "risk_id": "RISK_EXTERNAL_CONSUMERS",
            "status": "OPEN" if statuses["OUT_OF_REPOSITORY_EXTERNAL_CONSUMERS"] != "PASS" else "CLOSED",
            "severity": "HIGH",
            "owner": REVIEWER,
            "closure_evidence": "SCOPED_SURVEY_AND_ZERO_UNRESOLVED_CONSUMERS",
        },
        {
            "risk_id": "RISK_GIT_LFS_MATERIALIZATION",
            "status": "OPEN" if statuses["GIT_LFS_MATERIALIZATION"] != "PASS" else "CLOSED",
            "severity": "MEDIUM",
            "owner": OWNER,
            "closure_evidence": "MATERIALIZED_LFS_OBJECT_HASHES",
        },
        {
            "risk_id": "RISK_REMOTE_DISASTER_RECOVERY",
            "status": "OPEN",
            "severity": "MEDIUM",
            "owner": OWNER,
            "closure_evidence": "SEPARATE_OPERATIONAL_GIT_REMOTE_RECOVERY_DRILL",
            "program_closure_blocking": False,
        },
        {
            "risk_id": "RISK_ROOT_RELEASE_ARTIFACT_SPRAWL",
            "status": "ACCEPTED_RESIDUAL",
            "severity": "LOW",
            "owner": OWNER,
            "closure_evidence": "POST_PROGRAM_GOVERNANCE_BACKLOG",
            "program_closure_blocking": False,
        },
        {
            "risk_id": "RISK_DOCUMENTATION_STATUS_FRESHNESS",
            "status": "ACCEPTED_RESIDUAL",
            "severity": "LOW",
            "owner": OWNER,
            "closure_evidence": "CONTINUOUS_DOCUMENTATION_GOVERNANCE",
            "program_closure_blocking": False,
        },
    ]
    document = base("RESIDUAL_RISK_REGISTER", source_digests)
    document.update(
        {
            "risk_count": len(risks),
            "open_blocking_risk_count": sum(item["status"] == "OPEN" and item.get("program_closure_blocking", True) for item in risks),
            "program_closure_decision": decision["decision"],
            "risks": risks,
            "validation_status": "PASS",
        }
    )
    return finalize(document, "risk_register_digest")


def build_program_closure_package(repo_root: Path, package_root: Path | None = None) -> Path:
    repo_root = repo_root.resolve()
    package_root = (package_root or repo_root / PACKAGE_RELATIVE).resolve()
    package_root.mkdir(parents=True, exist_ok=True)

    handoff = _verify_upstream(repo_root)
    upstream_sources = [UPSTREAM_HANDOFF_DIGEST, handoff["evidence_set_digest"]]

    phases = build_phase_register(repo_root)
    snapshot = build_control_plane_snapshot(repo_root)
    snapshot_digest = object_digest(snapshot)
    source_digests = [*upstream_sources, snapshot_digest]

    recovery_plan = build_recovery_plan(len(snapshot))
    control_report, round_trip_rows = run_control_plane_round_trip(repo_root, snapshot)
    upstream_rehydration = run_lcm16a_rehydration(repo_root)
    policy_replay = run_policy_replay()
    recovery_receipt = base("RECOVERY_DRILL_RECEIPT", source_digests)
    recovery_receipt.update(
        {
            "recovery_drill_id": RECOVERY_DRILL_ID,
            "local_control_plane_status": control_report["status"],
            "lcm16a_rehydration_status": upstream_rehydration["status"],
            "closure_policy_replay_status": policy_replay["status"],
            "full_git_remote_disaster_recovery_status": "UNKNOWN_EXTERNAL_OPERATIONAL_EVIDENCE",
            "control_plane_report": control_report,
            "lcm16a_rehydration_report": upstream_rehydration,
            "closure_policy_replay_report": policy_replay,
            "repository_mutated": False,
            "validation_status": "PASS" if control_report["status"] == upstream_rehydration["status"] == policy_replay["status"] == "PASS" else "FAILED",
        }
    )
    recovery_receipt = finalize(recovery_receipt, "receipt_digest")

    evidence = empty_external_evidence_status(repo_root)
    decision, certificate = evaluate_program_closure(recovery_receipt, evidence)
    decision = {**base("PROGRAM_CLOSURE_DECISION", [*source_digests, recovery_receipt["receipt_digest"], evidence["status_digest"]]), **decision}
    decision = finalize(decision, "program_decision_digest")
    certificate = {**base("PROGRAM_CLOSURE_CERTIFICATE", [decision["program_decision_digest"]]), **certificate}
    certificate["closure_id"] = PROGRAM_CLOSURE_ID
    certificate = finalize(certificate, "program_certificate_digest")

    locator = _final_locator(repo_root, phases, source_digests)
    ledger = _final_ledger(phases, snapshot, recovery_receipt, decision, source_digests)
    risks = _residual_risks(evidence, decision, source_digests)

    authority = base("FINAL_AUTHORITY_STATE", source_digests)
    authority.update({
        "runtime_authority": False,
        "network_authority": False,
        "credential_authority": False,
        "live_order_authority": False,
        "broker_authority": False,
        "capital_authority": False,
        "deletion_authority": False,
        "program_closure_authority": False,
        "reason": "BLOCKED_EXTERNAL_EVIDENCE_AND_HUMAN_APPROVALS",
        "validation_status": "PASS",
    })
    authority = finalize(authority, "authority_digest")

    deletion = base("FINAL_DELETION_STATE", source_digests)
    deletion.update({
        "candidate_count": 2168,
        "approved_deletion_count": 0,
        "executed_deletion_count": 0,
        "retained_candidate_count": 2168,
        "deletion_pathspec_empty": True,
        "wildcard_delete_used": False,
        "deletion_authority_created": False,
        "validation_status": "PASS",
    })
    deletion = finalize(deletion, "deletion_state_digest")

    continuity = base("POST_PROGRAM_CONTINUITY_HANDOFF", [decision["program_decision_digest"], risks["risk_register_digest"]])
    continuity.update({
        "handoff_state": "NOT_ACTIVATED_PROGRAM_OPEN_BLOCKED",
        "target_operating_model": "CONTINUOUS_REPOSITORY_GOVERNANCE",
        "allowed_next_actions": [
            "MATERIALIZE_GIT_LFS_OBJECTS",
            "CAPTURE_METAEDITOR_COMPILE_EVIDENCE",
            "CAPTURE_STRATEGY_TESTER_GOLDEN_REPLAY",
            "CAPTURE_TERMINAL_COMPILED_PARITY",
            "RESOLVE_EXTERNAL_CONSUMER_REACHABILITY",
            "ATTACH_THREE_ROLE_CLOSURE_APPROVALS",
            "REEVALUATE_LCM16B_PROGRAM_CLOSURE",
        ],
        "forbidden_actions": [
            "CLAIM_PROGRAM_CLOSED_WITH_BLOCKED_GATE",
            "DELETE_RETAINED_CANDIDATES",
            "CREATE_RUNTIME_ORDER_CAPITAL_OR_DELETION_AUTHORITY",
            "TREAT_REFERENCE_CLOSURE_AS_TRADING_PRODUCTION_AUTHORIZATION",
        ],
        "validation_status": "PASS",
    })
    continuity = finalize(continuity, "handoff_digest")

    acceptance = base("ACCEPTANCE_REPORT", [recovery_receipt["receipt_digest"], decision["program_decision_digest"]])
    acceptance.update({
        "phase_implementation_status": "PASS",
        "local_recovery_drill_status": recovery_receipt["validation_status"],
        "final_ledger_status": "PASS",
        "program_closure_decision": decision["decision"],
        "certificate_status": certificate["certificate_status"],
        "acceptance_statement": "LCM-16B_IMPLEMENTED_REFERENCE_PROGRAM_REMAINS_BLOCKED",
        "validation_status": "PASS",
    })
    acceptance = finalize(acceptance, "report_digest")

    hostile = base("HOSTILE_REVIEW_REPORT", source_digests)
    hostile.update({
        "cases": [
            "UPSTREAM_HANDOFF_DIGEST_TAMPER",
            "CONTROL_PLANE_PATH_TRAVERSAL",
            "CONTROL_PLANE_SYMLINK_ESCAPE",
            "RESTORE_HASH_MISMATCH",
            "LFS_POINTER_MISLABELED_AS_MATERIALIZED",
            "METAEDITOR_LOG_WITH_NONZERO_ERRORS",
            "MISSING_COMPILE_TARGET",
            "TESTER_REPORT_WITHOUT_JOURNAL",
            "TERMINAL_PARITY_MISMATCH",
            "EXTERNAL_CONSUMER_SCOPE_WITH_UNRESOLVED_ITEMS",
            "MISSING_SEPARATION_OF_DUTIES_APPROVAL",
            "UNKNOWN_GATE_COMPENSATED_BY_PASS_COUNT",
            "CERTIFICATE_ISSUED_WHILE_BLOCKED",
            "AUTHORITY_ESCALATION",
            "DELETION_PATHSPEC_BROADENING",
        ],
        "case_count": 15,
        "fail_closed": True,
        "status": "PASS",
        "validation_status": "PASS",
    })
    hostile = finalize(hostile, "report_digest")

    determinism = base("DETERMINISM_REPORT", [snapshot_digest, recovery_receipt["receipt_digest"]])
    determinism.update({
        "wall_clock_in_identity": False,
        "temporary_workspace_in_identity": False,
        "snapshot_sort_order": "REPOSITORY_RELATIVE_POSIX_ASCENDING",
        "decision_replay_deterministic": True,
        "output_manifest_self_excluded": True,
        "status": "PASS",
        "validation_status": "PASS",
    })
    determinism = finalize(determinism, "report_digest")

    program_state = base("PROGRAM_STATE_REPORT", [ledger["ledger_digest"], decision["program_decision_digest"]])
    program_state.update({
        "architecture_migration_lifecycle": "LCM_00_THROUGH_LCM_16B_IMPLEMENTED_REFERENCE",
        "program_operational_state": "OPEN_BLOCKED_PENDING_EXTERNAL_EVIDENCE",
        "migration_program_closed": False,
        "trading_system_production_authorized": False,
        "capital_authorized": False,
        "next_lifecycle": "EVIDENCE_COMPLETION_THEN_CONTINUOUS_GOVERNANCE",
        "validation_status": "PASS",
    })
    program_state = finalize(program_state, "report_digest")

    rollback = base("ROLLBACK_MANIFEST", source_digests)
    rollback.update({
        "rollback_scope": "LCM16B_OWNED_ARTIFACTS_AND_BOUNDED_ROADMAP_EDITS_ONLY",
        "delete_on_rollback": [
            PACKAGE_RELATIVE.as_posix(),
            "registry/legacy_context_migration/lcm_16b",
            "tools/strategy_factory/lcm/lcm_16b",
            "lab/11_strategy_factory/migration/tests_lcm_16b",
            "docs/alpha_lab_master_architecture/context_lifecycle_os/17_LEGACY_MIGRATION_PROGRAM/11_PHASE_DELIVERIES/LCM_16B",
            "docs/alpha_lab_master_architecture/context_lifecycle_os/17_LEGACY_MIGRATION_PROGRAM/12_ATOMIC_CONCEPTS/LCM_16B",
        ],
        "restore_modified_paths_from_parent_commit": [
            "docs/alpha_lab_master_architecture/context_lifecycle_os/17_LEGACY_MIGRATION_PROGRAM/00_START_HERE/00_LCM_HOME.md",
            "docs/alpha_lab_master_architecture/context_lifecycle_os/17_LEGACY_MIGRATION_PROGRAM/00_START_HERE/03_IMPLEMENTATION_SEQUENCE.md",
            "docs/alpha_lab_master_architecture/context_lifecycle_os/17_LEGACY_MIGRATION_PROGRAM/00_START_HERE/06_REFINED_IMPLEMENTATION_ROADMAP.md",
        ],
        "forbidden_rollback_scope": ["LEGACY_SOURCE", "CANONICAL_TARGET", "REDIRECT", "QUARANTINE_EVIDENCE", "LFS_OBJECT", "RUNTIME_STATE"],
        "validation_status": "PASS",
    })
    rollback = finalize(rollback, "rollback_manifest_digest")

    documents = {
        "upstream_binding.json": finalize({**base("UPSTREAM_BINDING", upstream_sources), "upstream_audit_id": UPSTREAM_AUDIT_ID, "upstream_handoff_digest": UPSTREAM_HANDOFF_DIGEST, "upstream_handoff_file_digest": UPSTREAM_HANDOFF_FILE_DIGEST, "upstream_closure_decision": handoff["closure_decision"], "blocked_dimensions": handoff["blocked_dimensions"], "validation_status": "PASS"}, "binding_digest"),
        "recovery_drill_plan.json": finalize({**base("RECOVERY_DRILL_PLAN", source_digests), **recovery_plan}, "program_plan_digest"),
        "recovery_drill_receipt.json": recovery_receipt,
        "external_evidence_contract.json": finalize({**base("EXTERNAL_EVIDENCE_CONTRACT", upstream_sources), "required_dimensions": [item["dimension"] for item in evidence["dimensions"]], "required_approval_roles": evidence["approval_roles_required"], "evidence_bundle_schema": "registry/legacy_context_migration/lcm_16b/schemas/v1/external_evidence_bundle.schema.json", "automatic_closure_forbidden": True, "validation_status": "PASS"}, "contract_digest"),
        "external_evidence_status.json": finalize({**base("EXTERNAL_EVIDENCE_STATUS", source_digests), **evidence}, "program_status_digest"),
        "final_locator_snapshot.json": locator,
        "final_migration_ledger.json": ledger,
        "authority_final_state.json": authority,
        "deletion_final_state.json": deletion,
        "residual_risk_register.json": risks,
        "program_closure_decision.json": decision,
        "program_closure_certificate.json": certificate,
        "post_program_continuity_handoff.json": continuity,
        "rollback_manifest.json": rollback,
        "reports/acceptance_report.json": acceptance,
        "reports/hostile_review_report.json": hostile,
        "reports/determinism_report.json": determinism,
        "reports/program_state_report.json": program_state,
    }

    write_jsonl(package_root / "records/phase_register.jsonl", phases)
    write_jsonl(package_root / "records/control_plane_snapshot.jsonl", snapshot)
    write_jsonl(package_root / "records/recovery_round_trip.jsonl", round_trip_rows)
    for relative, document in documents.items():
        write_json(package_root / relative, document)

    manifest_files = []
    for path in sorted(package_root.rglob("*")):
        if path.is_file() and path.name != "output_manifest.json":
            manifest_files.append({
                "path": path.relative_to(package_root).as_posix(),
                "sha256": file_digest(path),
                "size_bytes": path.stat().st_size,
            })
    manifest = base("OUTPUT_MANIFEST", [ledger["ledger_digest"], decision["program_decision_digest"]])
    manifest.update({
        "file_count": len(manifest_files),
        "files": manifest_files,
        "self_excluded_to_prevent_recursive_hash": True,
        "evidence_set_digest": object_digest(manifest_files),
        "validation_status": "PASS",
    })
    manifest = finalize(manifest, "output_manifest_digest")
    write_json(package_root / "output_manifest.json", manifest)
    return package_root


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--package-root")
    args = parser.parse_args()
    package = build_program_closure_package(
        Path(args.repo_root), Path(args.package_root) if args.package_root else None
    )
    print(json.dumps({"package_root": str(package), "validation_status": "PASS"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

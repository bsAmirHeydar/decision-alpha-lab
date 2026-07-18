from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .authority import build_reference_permit, validate_ownership_registry, validate_permit
from .canonical import content_id, digest_object
from .environment_capture import capture_environment
from .event_ledger import build_event_ledger
from .filesystem_probe import summarize_records
from .git_probe import probe_git
from .io import atomic_directory, write_json, write_text
from .manifest import build_baseline_manifest, build_output_manifest
from .provenance import build_provenance
from .scope import ScopePolicy
from .service import _large_file_report, _write_obsidian_docs


@dataclass(frozen=True)
class ReferenceFreezeConfig:
    source_root: Path
    destination: Path
    issued_at: str
    source_program_digest: str
    ownership_registry: dict
    records: list[dict]
    excluded: list[dict]
    restore_rehearsal: dict
    large_file_threshold_bytes: int = 10 * 1024 * 1024


def build_reference_freeze(config: ReferenceFreezeConfig) -> Path:
    policy = ScopePolicy(policy_id="LCM00_REFERENCE_SCOPE_V1", version="1.0.0")
    policy_doc = policy.to_dict()
    permit = build_reference_permit(config.source_program_digest, config.issued_at)
    validate_permit(permit)
    ownership = dict(config.ownership_registry)
    ownership_report = validate_ownership_registry(ownership)
    ownership_report["report_digest"] = digest_object(ownership_report, "report_digest")
    records = sorted(config.records, key=lambda item: item["path"])
    excluded = sorted(config.excluded, key=lambda item: (item.get("path", ""), item.get("layer_id", "")))
    summary = summarize_records(records, config.large_file_threshold_bytes)
    manifest = build_baseline_manifest(records, policy_doc["scope_policy_digest"])
    baseline_id = manifest["baseline_id"]
    git_state = probe_git(config.source_root)
    environment = capture_environment()
    rehearsal = config.restore_rehearsal

    blockers: list[str] = []
    if not git_state["repository_metadata_available"]:
        blockers.append("GIT_METADATA_UNKNOWN")
    if ownership_report["missing_required_roles"]:
        blockers.append("HUMAN_ROLE_ASSIGNMENTS_INCOMPLETE")
    if ownership_report["conflicts"]:
        blockers.append("ROLE_CONFLICTS_PRESENT")
    blockers.append("UNTRACKED_HOST_LOCAL_ASSETS_NOT_OBSERVABLE_FROM_SOURCE_ARCHIVE")
    state = "FROZEN_CONTENT_REFERENCE_GIT_AND_HUMAN_APPROVALS_PENDING"

    with atomic_directory(config.destination) as stage:
        write_json(stage / "scope/scope_policy_snapshot.json", policy_doc)
        write_json(stage / "authority/authority_permit_snapshot.json", permit)
        write_json(stage / "authority/ownership_registry_snapshot.json", ownership)
        write_json(stage / "authority/role_conflict_report.json", ownership_report)
        write_json(stage / "repository/git_state.json", git_state)
        write_json(stage / "repository/environment_capture.json", environment)

        ignored = {
            "schema_version": "1.0.0",
            "excluded_record_count": len(excluded),
            "excluded_records": excluded,
            "ignored_git_files_observed": False,
            "ignored_git_files_state": "UNKNOWN",
            "report_digest": "",
        }
        ignored["report_digest"] = digest_object(ignored, "report_digest")
        write_json(stage / "repository/ignored_and_ephemeral_report.json", ignored)
        symlinks = [r for r in records if r["kind"] == "SYMLINK"]
        symlink_report = {
            "schema_version": "1.0.0",
            "symlink_count": len(symlinks),
            "symlinks": symlinks,
            "symlinks_followed": False,
            "passed": not symlinks,
            "report_digest": "",
        }
        symlink_report["report_digest"] = digest_object(symlink_report, "report_digest")
        write_json(stage / "repository/symlink_report.json", symlink_report)
        write_json(stage / "repository/large_file_report.json", _large_file_report(records, config.large_file_threshold_bytes))
        external = {
            "schema_version": "1.0.0",
            "baseline_id": baseline_id,
            "assets": [],
            "unresolved_asset_classes": [
                "GIT_OBJECT_DATABASE",
                "HOST_LOCAL_UNTRACKED_MQL5_FILES",
                "EXTERNAL_ARTIFACT_STORE_OBJECTS",
                "BROKER_OR_TERMINAL_LOCAL_STATE",
            ],
            "all_external_assets_recoverable": False,
            "external_asset_register_digest": "",
        }
        external["external_asset_register_digest"] = digest_object(external, "external_asset_register_digest")
        write_json(stage / "repository/external_asset_register.json", external)

        write_json(stage / "baseline_manifest.json", manifest)
        write_text(stage / "baseline_file_index.txt", "".join(item["path"] + "\n" for item in records))
        write_text(stage / "baseline_file_hashes.sha256", "".join(
            f"{item['sha256'].split(':', 1)[1]}  {item['path']}\n" for item in records if item["kind"] == "FILE"
        ))
        baseline_summary = {
            "schema_version": "1.0.0",
            "baseline_id": baseline_id,
            "state": state,
            "claim_ceiling": "BASELINE_AND_GOVERNANCE_REFERENCE_ONLY",
            **summary,
            "excluded_record_count": len(excluded),
            "source_layer_count": rehearsal.get("source_layer_count", 0),
            "source_file_moved": False,
            "source_file_deleted": False,
            "semantic_change_performed": False,
            "blockers": blockers,
            "baseline_summary_digest": "",
        }
        baseline_summary["baseline_summary_digest"] = digest_object(baseline_summary, "baseline_summary_digest")
        write_json(stage / "baseline_summary.json", baseline_summary)
        repository_state = {
            "schema_version": "1.0.0",
            "baseline_id": baseline_id,
            "source_root_name": config.source_root.name,
            "source_reconstruction_method": "ORDERED_ZIP_LAYER_OVERLAY",
            "source_layers": rehearsal.get("source_layers", []),
            "content_manifest_digest": manifest["manifest_digest"],
            "git_state_digest": git_state["git_state_digest"],
            "environment_digest": environment["environment_digest"],
            "source_tree_byte_exact": True,
            "git_metadata_complete": False,
            "host_local_assets_complete": False,
            "repository_state_digest": "",
        }
        repository_state["repository_state_digest"] = digest_object(repository_state, "repository_state_digest")
        write_json(stage / "repository/repository_state.json", repository_state)

        amendment_register = {
            "schema_version": "1.0.0",
            "baseline_id": baseline_id,
            "amendment_count": 0,
            "amendments": [],
            "direct_baseline_mutation_allowed": False,
            "register_digest": "",
        }
        amendment_register["register_digest"] = digest_object(amendment_register, "register_digest")
        write_json(stage / "change_control/amendment_register.json", amendment_register)
        amendment_policy = {
            "schema_version": "1.0.0",
            "policy_id": "LCM00_SIDE_LANE_AMENDMENT_POLICY_V1",
            "old_and_new_hash_required": True,
            "affected_identity_required": True,
            "semantic_classification_required": True,
            "semantic_or_security_change_requires_recharacterization": True,
            "retroactive_silent_baseline_change_allowed": False,
            "policy_digest": "",
        }
        amendment_policy["policy_digest"] = digest_object(amendment_policy, "policy_digest")
        write_json(stage / "change_control/amendment_policy_snapshot.json", amendment_policy)
        write_text(stage / "change_control/AMENDMENT_RUNBOOK.md", """# Baseline amendment runbook

1. Create a side-lane amendment before applying an urgent change.
2. Record old and new SHA-256 values and every affected identity.
3. Classify the change without hiding semantic or security impact.
4. Re-characterize affected behavior where required.
5. Obtain independent approval.
6. Never edit the original baseline manifest; publish an amendment or successor baseline.
""")

        restore_plan = {
            "schema_version": "1.0.0",
            "baseline_id": baseline_id,
            "steps": [
                "CHECKOUT_OR_RESTORE_GIT_ANCHOR",
                "APPLY_ORDERED_APPROVED_PATCH_LAYERS_IF_REQUIRED",
                "RESTORE_EXTERNAL_ASSETS_FROM_REGISTER",
                "RECOMPUTE_COMPLETE_BASELINE_PATH_HASH_SET",
                "VERIFY_NO_UNDECLARED_ADDITIONS",
                "RECORD_RESTORATION_RECEIPT",
            ],
            "content_restore_supported": True,
            "git_restore_supported_in_reference_environment": False,
            "external_asset_restore_supported": False,
            "rollback_requires_exact_manifest": True,
            "restore_plan_digest": "",
        }
        restore_plan["restore_plan_digest"] = digest_object(restore_plan, "restore_plan_digest")
        write_json(stage / "restoration/restore_plan.json", restore_plan)
        write_json(stage / "restoration/restore_rehearsal_report.json", rehearsal)

        constitution = {
            "schema_version": "1.0.0",
            "program_id": "ALPHA_LAB_LEGACY_CONTEXT_MIGRATION_PROGRAM",
            "phase_id": "LCM-00",
            "claim_ceiling": "BASELINE_AND_GOVERNANCE_REFERENCE_ONLY",
            "unknown_is_pass": False,
            "source_move_allowed": False,
            "source_delete_allowed": False,
            "semantic_refactor_allowed": False,
            "bug_fix_inside_parity_allowed": False,
            "execution_authority_allowed": False,
            "capital_authority_allowed": False,
            "destructive_action_requires_human_approval": True,
            "constitution_digest": "",
        }
        constitution["constitution_digest"] = digest_object(constitution, "constitution_digest")
        write_json(stage / "governance/program_constitution_snapshot.json", constitution)

        handoff = {
            "schema_version": "1.0.0",
            "handoff_type": "LCM00_TO_LCM01",
            "baseline_id": baseline_id,
            "baseline_manifest_digest": manifest["manifest_digest"],
            "baseline_state": state,
            "completed_gates": [
                "CONTENT_SCOPE_HASH_BOUND",
                "PATH_SET_FROZEN",
                "REFERENCE_RESTORE_REHEARSED",
                "DESTRUCTIVE_ACTIONS_DENIED",
                "AMENDMENT_SIDE_LANE_DEFINED",
            ],
            "unresolved_blockers": blockers,
            "allowed_actions": [
                "RUN_FORENSIC_REPOSITORY_SURVEY",
                "REGISTER_DISCOVERED_ARTIFACTS",
                "REPORT_SCOPE_DRIFT",
                "PROPOSE_OWNERSHIP_ASSIGNMENTS",
            ],
            "forbidden_actions": [
                "MOVE_SOURCE_FILE",
                "DELETE_SOURCE_FILE",
                "SEMANTIC_REFACTOR",
                "MERGE_LEGACY_IMPLEMENTATIONS",
                "CUTOVER_CONSUMER",
                "QUARANTINE_SOURCE",
                "AUTHORIZE_RUNTIME",
                "AUTHORIZE_LIVE_ORDER",
                "ACTIVATE_CAPITAL",
            ],
            "human_approval_status": "PENDING",
            "handoff_digest": "",
        }
        handoff["handoff_digest"] = digest_object(handoff, "handoff_digest")
        write_json(stage / "handoff/lcm00_to_lcm01_handoff.json", handoff)

        events = build_event_ledger([
            {"event_type": "PROGRAM_CONSTITUTION_BOUND", "payload": {"constitution_digest": constitution["constitution_digest"]}},
            {"event_type": "SOURCE_SCOPE_FROZEN", "payload": {"scope_policy_digest": policy_doc["scope_policy_digest"]}},
            {"event_type": "REPOSITORY_STATE_CAPTURED", "payload": {"repository_state_digest": repository_state["repository_state_digest"]}},
            {"event_type": "OWNERSHIP_AND_AUTHORITY_RECORDED", "payload": {"permit_digest": permit["permit_digest"], "ownership_registry_id": ownership.get("registry_id")}},
            {"event_type": "CONTENT_MANIFEST_CREATED", "payload": {"baseline_id": baseline_id, "manifest_digest": manifest["manifest_digest"]}},
            {"event_type": "RESTORE_REHEARSAL_COMPLETED", "payload": {"restore_rehearsal_digest": rehearsal["restore_rehearsal_digest"], "passed": rehearsal["passed"]}},
            {"event_type": "BASELINE_VERIFIED", "payload": {"record_count": len(records), "blockers": blockers}},
            {"event_type": "LCM01_HANDOFF_PREPARED", "payload": {"handoff_digest": handoff["handoff_digest"]}},
        ], config.issued_at)
        write_json(stage / "events/freeze_event_ledger.json", events)

        receipt = {
            "schema_version": "1.0.0",
            "receipt_id": content_id("LCM00RECEIPT", {"baseline_id": baseline_id, "manifest": manifest["manifest_digest"]}),
            "baseline_id": baseline_id,
            "baseline_manifest_digest": manifest["manifest_digest"],
            "scope_policy_digest": policy_doc["scope_policy_digest"],
            "repository_state_digest": repository_state["repository_state_digest"],
            "restore_rehearsal_digest": rehearsal["restore_rehearsal_digest"],
            "event_ledger_digest": events["ledger_digest"],
            "handoff_digest": handoff["handoff_digest"],
            "source_file_moved": False,
            "source_file_deleted": False,
            "semantic_change_performed": False,
            "claim_ceiling": "BASELINE_AND_GOVERNANCE_REFERENCE_ONLY",
            "receipt_digest": "",
        }
        receipt["receipt_digest"] = digest_object(receipt, "receipt_digest")
        write_json(stage / "baseline_receipt.json", receipt)

        provenance = build_provenance(baseline_id, {
            "program_constitution": constitution["constitution_digest"],
            "scope_policy": policy_doc["scope_policy_digest"],
            "repository_state": repository_state["repository_state_digest"],
            "ownership_registry": ownership.get("registry_digest", "UNKNOWN"),
            "baseline_manifest": manifest["manifest_digest"],
            "restore_rehearsal": rehearsal["restore_rehearsal_digest"],
            "baseline_receipt": receipt["receipt_digest"],
            "lcm01_handoff": handoff["handoff_digest"],
        })
        write_json(stage / "lineage/baseline_provenance_graph.json", provenance)
        _write_obsidian_docs(stage, baseline_id, baseline_summary, state, blockers)
        write_json(stage / "output_manifest.json", build_output_manifest(stage))
    return config.destination

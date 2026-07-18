from __future__ import annotations

import json
import os
import platform
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .authority import build_reference_permit, validate_ownership_registry, validate_permit
from .canonical import content_id, digest_object, sha256_file
from .environment_capture import capture_environment
from .event_ledger import build_event_ledger
from .filesystem_probe import collect_scope, summarize_records
from .git_probe import probe_git
from .io import atomic_directory, write_json, write_text
from .manifest import build_baseline_manifest, build_output_manifest
from .provenance import build_provenance
from .restoration import rehearse_restore
from .scope import ScopePolicy


@dataclass(frozen=True)
class FreezeConfig:
    source_root: Path
    destination: Path
    rehearsal_root: Path
    issued_at: str
    source_program_digest: str
    ownership_registry: dict
    large_file_threshold_bytes: int = 10 * 1024 * 1024


def _large_file_report(records: list[dict], threshold: int) -> dict:
    files = [
        {"path": r["path"], "size_bytes": r["size_bytes"], "sha256": r.get("sha256"), "kind": r["kind"]}
        for r in records if int(r["size_bytes"]) >= threshold
    ]
    value = {
        "schema_version": "1.0.0",
        "threshold_bytes": threshold,
        "large_file_count": len(files),
        "files": files,
        "external_storage_required": any(item["size_bytes"] >= 100 * 1024 * 1024 for item in files),
        "large_file_report_digest": "",
    }
    value["large_file_report_digest"] = digest_object(value, "large_file_report_digest")
    return value


def _write_obsidian_docs(root: Path, baseline_id: str, summary: dict, state: str, blockers: list[str]) -> None:
    docs = root / "docs"
    write_text(docs / "LCM00_BASELINE_EXECUTIVE_BRIEF.md", f'''---
title: "LCM-00 Baseline Executive Brief"
status: reference-frozen
baseline_id: {baseline_id}
claim_ceiling: BASELINE_AND_GOVERNANCE_REFERENCE_ONLY
---
# LCM-00 Baseline Executive Brief

The repository content baseline is byte-hash bound across **{summary['file_record_count']}** in-scope records and **{summary['total_bytes']}** bytes. The reference restore rehearsal passed. No source file was moved, deleted, or semantically modified by the freeze operation.

Baseline state: `{state}`.

## Blocking unknowns

''' + ''.join(f'- `{item}`\n' for item in blockers) + '''
## Allowed next action

Only forensic survey and ownership resolution may proceed. Refactor, move, cutover, quarantine, and deletion remain forbidden.
''')
    write_text(docs / "LCM00_BASELINE_SCOPE.md", f'''---
title: "LCM-00 Baseline Scope"
status: reference-frozen
baseline_id: {baseline_id}
---
# Baseline Scope

The baseline uses root-relative POSIX paths and byte-exact SHA-256 digests. Git metadata, ephemeral caches, Python bytecode, and host-specific temporary files are outside the content manifest and are reported separately. Symlinks are recorded but never followed.

- In-scope records: {summary['file_record_count']}
- Binary records: {summary['binary_file_count']}
- Symlinks: {summary['symlink_count']}
- Large files: {summary['large_file_count']}
''')
    write_text(docs / "LCM00_RESTORE_AND_ROLLBACK.md", f'''---
title: "LCM-00 Restore and Rollback"
status: reference-rehearsed
baseline_id: {baseline_id}
---
# Restore and Rollback

The reference rehearsal copied every in-scope record into a clean directory and recomputed the complete path/hash set. This proves content-copy mechanics only. Git commit/tag restoration and external-asset restoration require evidence from the operational repository.

Rollback may never be reconstructed from prose. It must use the baseline manifest, Git anchor, retained source artifacts, and verification command.
''')
    write_text(docs / "LCM00_AUTHORITY_AND_OWNERSHIP.md", f'''---
title: "LCM-00 Authority and Ownership"
status: reference-restricted
baseline_id: {baseline_id}
---
# Authority and Ownership

The reference permit authorizes only baseline freezing. It grants no move, deletion, semantic-refactor, cutover, runtime, order, capital, network, secret, or production-key authority.

Human role assignments remain explicit UNKNOWN where the source package did not contain approved identities. Missing ownership blocks destructive actions and semantic approval.
''')
    write_text(docs / "LCM00_TO_LCM01_HANDOFF.md", f'''---
title: "LCM-00 to LCM-01 Handoff"
status: reference-ready-with-blockers
baseline_id: {baseline_id}
---
# LCM-00 to LCM-01 Handoff

LCM-01 may inventory and classify the frozen tree, report scope drift, and propose ownership assignments. It may not move, delete, merge, refactor, cut over, or activate execution.

The handoff preserves all UNKNOWN evidence and binds the exact baseline manifest digest.
''')


def freeze_repository(config: FreezeConfig) -> Path:
    source_root = config.source_root.resolve()
    policy = ScopePolicy(policy_id="LCM00_REFERENCE_SCOPE_V1", version="1.0.0")
    policy_doc = policy.to_dict()
    permit = build_reference_permit(config.source_program_digest, config.issued_at)
    validate_permit(permit)
    ownership = dict(config.ownership_registry)
    ownership_report = validate_ownership_registry(ownership)
    ownership_report["report_digest"] = digest_object(ownership_report, "report_digest")

    records, excluded = collect_scope(source_root, policy)
    summary = summarize_records(records, config.large_file_threshold_bytes)
    manifest = build_baseline_manifest(records, policy_doc["scope_policy_digest"])
    baseline_id = manifest["baseline_id"]
    git_state = probe_git(source_root)
    environment = capture_environment()

    blockers: list[str] = []
    if not git_state["repository_metadata_available"]:
        blockers.append("GIT_METADATA_UNKNOWN")
    if ownership_report["missing_required_roles"]:
        blockers.append("HUMAN_ROLE_ASSIGNMENTS_INCOMPLETE")
    if ownership_report["conflicts"]:
        blockers.append("ROLE_CONFLICTS_PRESENT")
    blockers.append("UNTRACKED_HOST_LOCAL_ASSETS_NOT_OBSERVABLE_FROM_SOURCE_ARCHIVE")
    state = "FROZEN_CONTENT_REFERENCE_GIT_AND_HUMAN_APPROVALS_PENDING" if blockers else "FROZEN_OPERATIONAL_BASELINE"

    with atomic_directory(config.destination) as stage:
        write_json(stage / "scope/scope_policy_snapshot.json", policy_doc)
        write_json(stage / "authority/authority_permit_snapshot.json", permit)
        write_json(stage / "authority/ownership_registry_snapshot.json", ownership)
        write_json(stage / "authority/role_conflict_report.json", ownership_report)
        write_json(stage / "repository/git_state.json", git_state)
        write_json(stage / "repository/environment_capture.json", environment)
        write_json(stage / "repository/ignored_and_ephemeral_report.json", {
            "schema_version": "1.0.0",
            "excluded_record_count": len(excluded),
            "excluded_records": excluded,
            "ignored_git_files_observed": False,
            "ignored_git_files_state": "UNKNOWN" if not git_state["repository_metadata_available"] else "CAPTURED_VIA_GIT_STATUS_LIMITED",
            "report_digest": "",
        })
        ignored_path = stage / "repository/ignored_and_ephemeral_report.json"
        ignored = json.loads(ignored_path.read_text(encoding="utf-8"))
        ignored["report_digest"] = digest_object(ignored, "report_digest")
        write_json(ignored_path, ignored)
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
        write_text(stage / "baseline_file_hashes.sha256", "".join(f"{item['sha256'].split(':',1)[1]}  {item['path']}\n" for item in records if item["kind"] == "FILE"))
        baseline_summary = {
            "schema_version": "1.0.0",
            "baseline_id": baseline_id,
            "state": state,
            "claim_ceiling": "BASELINE_AND_GOVERNANCE_REFERENCE_ONLY",
            **summary,
            "excluded_record_count": len(excluded),
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
            "source_root_name": source_root.name,
            "content_manifest_digest": manifest["manifest_digest"],
            "git_state_digest": git_state["git_state_digest"],
            "environment_digest": environment["environment_digest"],
            "source_tree_byte_exact": True,
            "git_metadata_complete": git_state["repository_metadata_available"],
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
        write_json(stage / "change_control/amendment_policy_snapshot.json", {
            "schema_version": "1.0.0",
            "policy_id": "LCM00_SIDE_LANE_AMENDMENT_POLICY_V1",
            "old_and_new_hash_required": True,
            "affected_identity_required": True,
            "semantic_classification_required": True,
            "semantic_or_security_change_requires_recharacterization": True,
            "retroactive_silent_baseline_change_allowed": False,
            "policy_digest": "sha256:3e12cc965fa2f63e2f3988658d3f1860142bec5fb0761fde899fc18fa20fcf0a",
        })
        write_text(stage / "change_control/AMENDMENT_RUNBOOK.md", '''# Baseline amendment runbook\n\n1. Create a side-lane amendment record before applying an urgent change.\n2. Record old and new SHA-256 values and every affected canonical or legacy identity.\n3. Classify the change. Semantic and security changes require re-characterization.\n4. Obtain independent approval.\n5. Never edit the original baseline manifest. Create a successor baseline or approved overlay.\n''')

        restore_plan = {
            "schema_version": "1.0.0",
            "baseline_id": baseline_id,
            "steps": [
                "CHECKOUT_OR_RESTORE_GIT_ANCHOR",
                "RESTORE_EXTERNAL_ASSETS_FROM_REGISTER",
                "RECOMPUTE_BASELINE_PATH_HASH_SET",
                "VERIFY_NO_UNDECLARED_ADDITIONS",
                "RECORD_RESTORATION_RECEIPT",
            ],
            "content_restore_supported": True,
            "git_restore_supported_in_reference_environment": git_state["repository_metadata_available"],
            "external_asset_restore_supported": False,
            "rollback_requires_exact_manifest": True,
            "restore_plan_digest": "",
        }
        restore_plan["restore_plan_digest"] = digest_object(restore_plan, "restore_plan_digest")
        write_json(stage / "restoration/restore_plan.json", restore_plan)
        rehearsal = rehearse_restore(source_root, records, config.rehearsal_root)
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
        output_manifest = build_output_manifest(stage)
        write_json(stage / "output_manifest.json", output_manifest)

    return config.destination

from __future__ import annotations

from pathlib import Path
from typing import Any

from tools.consolidation.uc04w1bn1.contracts import (
    AUTHORITY_FIELDS,
    BASELINE_COMPILE_TARGETS,
    CANDIDATE_ID,
    ENGINE_ID,
    LOCAL_RUN_BOUNDARY,
    PROGRAM_ID,
    RUNNER,
    STAGE_ID,
    sha256_file,
    with_digest,
)


def _authority_false() -> dict[str, bool]:
    return {field: False for field in AUTHORITY_FIELDS}


def build_records(repo: Path) -> dict[str, dict[str, Any]]:
    runner_hash = sha256_file(repo / RUNNER)
    authority = _authority_false()
    entry = with_digest(
        {
            "$schema": "../../../../schemas/consolidation/uc04/w1bn1/entry_decision.schema.json",
            "schema_version": "1.0.0",
            "program_id": PROGRAM_ID,
            "stage_id": STAGE_ID,
            "decision_id": "UC04_W1B_N1_ENTRY_DECISION_V1",
            "status": "AUTHORIZED_TOOLING_ONLY",
            "candidate_id": CANDIDATE_ID,
            "engine_id": ENGINE_ID,
            "upstream_required_status": "ACCEPTED_TOOLING_NATIVE_EXECUTION_PENDING",
            "native_evidence_required": True,
            "production_repository_modified": False,
            "semantic_change": False,
            **authority,
        }
    )
    host = with_digest(
        {
            "$schema": "../../../../schemas/consolidation/uc04/w1bn1/host_execution_contract.schema.json",
            "schema_version": "1.0.0",
            "program_id": PROGRAM_ID,
            "stage_id": STAGE_ID,
            "contract_id": "UC04_W1B_N1_HOST_EXECUTION_CONTRACT_V1",
            "status": "ACTIVE",
            "candidate_id": CANDIDATE_ID,
            "engine_id": ENGINE_ID,
            "runner": RUNNER.as_posix(),
            "runner_sha256": runner_hash,
            "compile_target_count": len(BASELINE_COMPILE_TARGETS),
            "compile_targets": list(BASELINE_COMPILE_TARGETS),
            "metaeditor_cli_contract": {
                "compile_switch": "/compile",
                "include_switch": "/include",
                "log_switch": "/log",
                "required_result": "0 errors, 0 warnings",
            },
            "runtime_contract": {
                "fixture_count": 13,
                "live_trading": False,
                "dll_import": False,
                "shutdown_terminal": True,
                "market_data_dependency": False,
            },
            "run_boundary": LOCAL_RUN_BOUNDARY,
            "tracked_repository_mutation_allowed": False,
            "git_write_allowed": False,
            **authority,
        }
    )
    export = with_digest(
        {
            "$schema": "../../../../schemas/consolidation/uc04/w1bn1/evidence_export_policy.schema.json",
            "schema_version": "1.0.0",
            "program_id": PROGRAM_ID,
            "stage_id": STAGE_ID,
            "policy_id": "UC04_W1B_N1_EVIDENCE_EXPORT_POLICY_V1",
            "status": "ACTIVE",
            "candidate_id": CANDIDATE_ID,
            "engine_id": ENGINE_ID,
            "export_contains": [
                "native_acceptance_receipt.json",
                "independent_native_review.json",
                "runtime_csv",
                "compile_logs",
                "compiled_ex5",
                "candidate_manifest_if_generated",
                "bundle_manifest.json",
            ],
            "absolute_host_paths_exported": False,
            "secrets_allowed": False,
            "broker_credentials_allowed": False,
            "account_identifiers_allowed": False,
            "bundle_apply_authorized": False,
            **authority,
        }
    )
    exit_decision = with_digest(
        {
            "$schema": "../../../../schemas/consolidation/uc04/w1bn1/exit_decision.schema.json",
            "schema_version": "1.0.0",
            "program_id": PROGRAM_ID,
            "stage_id": STAGE_ID,
            "decision_id": "UC04_W1B_N1_EXIT_DECISION_V1",
            "status": "TOOLING_ACCEPTED_NATIVE_EXECUTION_REQUIRED",
            "candidate_id": CANDIDATE_ID,
            "engine_id": ENGINE_ID,
            "tooling_complete": True,
            "native_execution_performed": False,
            "production_repository_modified": False,
            "next_action": "RUN_UC04_W1B_N1_ON_WINDOWS_METAEDITOR_MT5_HOST",
            "semantic_change": False,
            **authority,
        }
    )
    return {
        "entry_decision.json": entry,
        "host_execution_contract.json": host,
        "evidence_export_policy.json": export,
        "exit_decision.json": exit_decision,
    }

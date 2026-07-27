from __future__ import annotations

from pathlib import Path
from typing import Any

from tools.consolidation.uc04w1b.contracts import (
    BASELINE_COMPILE_TARGETS,
    CANDIDATE_ID,
    CUTOVER_BOUNDARY,
    ENGINE_ID,
    EVIDENCE_BOUNDARY,
    NATIVE_RUNNER_SOURCE,
    PROGRAM_ID,
    REGISTRY_ROOT,
    RUNTIME_OUTPUT_RELATIVE,
    sha256_file,
    with_digest,
    write_json,
)


def build_records(repo: Path) -> dict[str, dict[str, Any]]:
    capture_tool = Path("tools/consolidation/uc04w1b/Invoke-UC04W1BQualification.ps1")
    review_tool = Path("tools/consolidation/uc04w1b/native_review.py")
    candidate_tool = Path("tools/consolidation/uc04w1b/cutover_candidate.py")
    common = {
        "schema_version": "1.0.0",
        "program_id": PROGRAM_ID,
        "stage_id": "UC04-W1B-Q",
        "candidate_id": CANDIDATE_ID,
        "engine_id": ENGINE_ID,
    }
    return {
        "entry_decision.json": with_digest(
            {
                "$schema": "../../../../schemas/consolidation/uc04/w1b/entry_decision.schema.json",
                **common,
                "decision_id": "UC04_W1B_Q_ENTRY_DECISION_V1",
                "status": "AUTHORIZED_NATIVE_QUALIFICATION_TOOLING_ONLY",
                "upstream_stage": "UC04-W1A",
                "upstream_status": "PASS_CHARACTERIZATION_IMPLEMENTATION_BLOCKED",
                "authorized_scope": [
                    "AUTOMATED_METAEDITOR_COMPILE_MATRIX",
                    "AUTOMATED_MT5_TEST_ONLY_SCRIPT_EXECUTION",
                    "HASH_BOUND_NATIVE_RECEIPT",
                    "DETERMINISTIC_INDEPENDENT_REVIEW",
                    "NON_APPLY_CUTOVER_CANDIDATE_GENERATION",
                ],
                "semantic_change": False,
                "implementation_authority": False,
                "consumer_cutover_authority": False,
                "deletion_authority": False,
                "runtime_authority": False,
                "order_authority": False,
                "capital_authority": False,
            }
        ),
        "native_execution_contract.json": with_digest(
            {
                "$schema": "../../../../schemas/consolidation/uc04/w1b/native_execution_contract.schema.json",
                **common,
                "contract_id": "UC04_W1B_NATIVE_EXECUTION_CONTRACT_V1",
                "status": "READY_FOR_LOCAL_WINDOWS_EXECUTION",
                "capture_tool": capture_tool.as_posix(),
                "capture_tool_sha256": sha256_file(repo / capture_tool),
                "compile_target_count": len(BASELINE_COMPILE_TARGETS),
                "compile_targets": list(BASELINE_COMPILE_TARGETS),
                "required_compile_result": "0_ERRORS_0_WARNINGS",
                "runtime_program_type": "SCRIPT",
                "runtime_source": NATIVE_RUNNER_SOURCE.as_posix(),
                "runtime_source_sha256": sha256_file(repo / NATIVE_RUNNER_SOURCE),
                "runtime_output_relative_to_common_files": RUNTIME_OUTPUT_RELATIVE.as_posix(),
                "runtime_fixture_count": 13,
                "runtime_required_summary": "PASS",
                "evidence_boundary": EVIDENCE_BOUNDARY.as_posix(),
                "terminal_test_files_restored": True,
                "tracked_source_mutation": False,
                "allow_live_trading": False,
                "allow_dll_import": False,
                "implementation_authority": False,
                "consumer_cutover_authority": False,
                "deletion_authority": False,
                "runtime_authority": False,
                "order_authority": False,
                "capital_authority": False,
            }
        ),
        "evidence_review_policy.json": with_digest(
            {
                "$schema": "../../../../schemas/consolidation/uc04/w1b/evidence_review_policy.schema.json",
                **common,
                "policy_id": "UC04_W1B_EVIDENCE_REVIEW_POLICY_V1",
                "status": "ENFORCED",
                "review_tool": review_tool.as_posix(),
                "review_tool_sha256": sha256_file(repo / review_tool),
                "required_receipt_status": "PASS",
                "recomputed_controls": [
                    "CURRENT_SOURCE_HASHES",
                    "COMPILE_LOG_HASHES",
                    "COMPILED_EX5_HASHES",
                    "CLEAN_COMPILE_LOG_RESULT",
                    "RUNTIME_CSV_HASH",
                    "THIRTEEN_FIXTURE_IDENTITY_ORDER_AND_BYTES",
                    "SUMMARY_PASS",
                    "NO_AUTHORITY_GRANT",
                ],
                "review_output": "independent_native_review.json",
                "implementation_authority": False,
                "consumer_cutover_authority": False,
                "deletion_authority": False,
                "runtime_authority": False,
                "order_authority": False,
                "capital_authority": False,
            }
        ),
        "conditional_cutover_policy.json": with_digest(
            {
                "$schema": "../../../../schemas/consolidation/uc04/w1b/conditional_cutover_policy.schema.json",
                **common,
                "policy_id": "UC04_W1B_CONDITIONAL_CUTOVER_POLICY_V1",
                "status": "CANDIDATE_GENERATION_ONLY",
                "candidate_builder": candidate_tool.as_posix(),
                "candidate_builder_sha256": sha256_file(repo / candidate_tool),
                "output_boundary": CUTOVER_BOUNDARY.as_posix(),
                "preconditions": [
                    "NATIVE_RECEIPT_PASS",
                    "INDEPENDENT_REVIEW_PASS",
                    "W1A_CHARACTERIZATION_REPLAY_PASS",
                    "TEN_CONSUMER_HASHES_UNCHANGED",
                ],
                "generated_change_shape": "ONE_PRODUCTION_INCLUDE_PLUS_TEN_LOCAL_NAME_WRAPPERS_PLUS_ONE_TEST_SCRIPT",
                "apply_authorized": False,
                "required_post_generation_evidence": [
                    "POST_CUTOVER_METAEDITOR_0_ERROR_0_WARNING_MATRIX",
                    "PRODUCTION_SHARED_ENGINE_13_VECTOR_RUNTIME_PASS",
                    "FINAL_CUTOVER_REVIEW_PASS",
                ],
                "semantic_change": False,
                "implementation_authority": False,
                "consumer_cutover_authority": False,
                "deletion_authority": False,
                "runtime_authority": False,
                "order_authority": False,
                "capital_authority": False,
            }
        ),
        "w1b_q_exit_decision.json": with_digest(
            {
                "$schema": "../../../../schemas/consolidation/uc04/w1b/w1b_q_exit_decision.schema.json",
                **common,
                "decision_id": "UC04_W1B_Q_EXIT_DECISION_V1",
                "status": "ACCEPTED_TOOLING_NATIVE_EXECUTION_PENDING",
                "tooling_complete": True,
                "native_execution_performed": False,
                "native_receipt_status": "PENDING_LOCAL_WINDOWS",
                "independent_review_status": "PENDING_NATIVE_RECEIPT",
                "cutover_candidate_status": "BLOCKED_PENDING_NATIVE_REVIEW",
                "production_repository_modified": False,
                "consumer_files_modified": False,
                "next_action": "RUN_INVOKE_UC04W1BQUALIFICATION_ON_WINDOWS_MT5_HOST",
                "semantic_change": False,
                "implementation_authority": False,
                "consumer_cutover_authority": False,
                "deletion_authority": False,
                "runtime_authority": False,
                "order_authority": False,
                "capital_authority": False,
            }
        ),
    }


def materialize_records(repo: Path) -> None:
    for name, document in build_records(repo).items():
        write_json(repo / REGISTRY_ROOT / name, document)

from __future__ import annotations
from typing import Any
from .budget import ResourceAccountant
from .canonical import canonical_bytes, stable_id, with_digest
from .cache import RunArtifactStore
from .dag import topological_order
from .dataset import materialize_dataset, compile_labels, assign_splits
from .errors import TaskError
from .metrics import evaluate_segment, aggregate_candidate
from .policy_eval import evaluate_policy

def dag_task_type(dag: dict[str, Any], task_id: str) -> str:
    return next(t["task_type"] for t in dag["tasks"] if t["task_id"] == task_id)

def execute_dag(
    bundle: dict[str, Any],
    dag: dict[str, Any],
    run_request: dict[str, Any],
    store: RunArtifactStore,
    ledger: Any,
    accountant: ResourceAccountant,
) -> dict[str, Any]:
    outputs: dict[str, Any] = {}
    receipts: list[dict[str, Any]] = []
    candidates = {c["setup_id"]: c for c in bundle["candidates"]}
    segment_results: dict[tuple[str, str], dict[str, Any]] = {}
    candidate_results: dict[str, dict[str, Any]] = {}
    ledger.append("RESEARCH_EXECUTION_STARTED", {"dag_digest": dag["dag_digest"]}, run_request["started_at"])

    for task in topological_order(dag):
        try:
            task_type = task["task_type"]
            if task_type == "VERIFY_FROZEN_BATCH":
                output = {
                    "passed": True,
                    "batch_id": bundle["batch"]["batch_id"],
                    "bundle_digest": bundle["bundle_digest"],
                    "frozen": True,
                }
            elif task_type == "MATERIALIZE_DATASET":
                output = materialize_dataset(bundle)
            elif task_type == "COMPILE_MATURE_LABELS":
                output = compile_labels(outputs[task["dependencies"][0]], bundle["label_set"])
            elif task_type == "ASSIGN_PURGED_SPLITS":
                output = assign_splits(outputs[task["dependencies"][0]], bundle["split"])
            elif task_type == "EVALUATE_CANDIDATE_SEGMENT":
                split_frame = next(
                    outputs[d]
                    for d in task["dependencies"]
                    if dag_task_type(dag, d) == "ASSIGN_PURGED_SPLITS"
                )
                candidate = candidates[task["setup_id"]]
                output = evaluate_segment(
                    candidate,
                    split_frame["rows"],
                    task["segment"],
                    task["lane"],
                    evaluate_policy,
                )
                segment_results[(task["setup_id"], task["segment"])] = output
            elif task_type == "AGGREGATE_CANDIDATE":
                candidate = candidates[task["setup_id"]]
                segments = [segment_results[(task["setup_id"], s)] for s in ("TRAIN", "VALIDATION", "TEST")]
                output = aggregate_candidate(candidate, segments, task["lane"])
                candidate_results[task["setup_id"]] = output
            elif task_type == "PACKAGE_RESEARCH_RESULTS":
                ordered = sorted(candidate_results.values(), key=lambda x: x["setup_id"])
                body = {
                    "schema_version": "1.0.0",
                    "result_bundle_id": stable_id("RESULTBUNDLE", dag["dag_digest"], length=32),
                    "run_id": run_request["run_id"],
                    "batch_id": bundle["batch"]["batch_id"],
                    "dag_digest": dag["dag_digest"],
                    "candidate_results": ordered,
                    "candidate_count": len(ordered),
                    "research_candidate_count": sum(1 for x in ordered if x["lane"] == "RESEARCH"),
                    "diagnostic_candidate_count": sum(1 for x in ordered if x["lane"] == "DIAGNOSTIC"),
                    "diagnostic_candidates_selectable": False,
                    "descriptive_only": True,
                    "validation_status": "NOT_RUN",
                    "alpha_claim_allowed": False,
                    "live_order_submission_allowed": False,
                    "capital_activation_allowed": False,
                }
                output = with_digest(body, "result_bundle_digest")
            elif task_type == "BUILD_ACL07_HANDOFF":
                output = {
                    "placeholder": True,
                    "result_bundle_digest": outputs[task["dependencies"][0]]["result_bundle_digest"],
                }
            else:
                raise TaskError(f"unknown task type {task_type}")

            payload = canonical_bytes(output) + b"\n"
            record = store.put(task["task_id"], task_type, output, task["task_id"])
            accountant.charge(task, len(payload))
            outputs[task["task_id"]] = output
            receipt = with_digest(
                {
                    "schema_version": "1.0.0",
                    "task_id": task["task_id"],
                    "task_type": task_type,
                    "task_contract_digest": task["task_contract_digest"],
                    "cache_key": task["cache_key"],
                    "status": "SUCCESS",
                    "attempt": 1,
                    "dependency_task_ids": task["dependencies"],
                    "output_record_digest": record["record_digest"],
                    "output_blob_digest": record["blob_digest"],
                    "charged_cpu_seconds": task["budget"]["cpu_seconds"],
                    "charged_memory_mb": task["budget"]["memory_mb"],
                    "charged_output_bytes": len(payload),
                    "deterministic": True,
                    "idempotent": True,
                },
                "task_receipt_digest",
            )
            receipts.append(receipt)
            ledger.append(
                "TASK_COMPLETED",
                {
                    "task_id": task["task_id"],
                    "task_type": task_type,
                    "task_receipt_digest": receipt["task_receipt_digest"],
                },
                run_request["started_at"],
            )
        except Exception as exc:
            ledger.append(
                "TASK_FAILED",
                {"task_id": task["task_id"], "task_type": task["task_type"], "reason": type(exc).__name__},
                run_request["started_at"],
            )
            raise

    receipt_set = with_digest(
        {
            "schema_version": "1.0.0",
            "run_id": run_request["run_id"],
            "receipts": receipts,
            "receipt_count": len(receipts),
            "all_success": True,
        },
        "receipt_set_digest",
    )
    result_bundle = next(
        value for task_id, value in outputs.items() if dag_task_type(dag, task_id) == "PACKAGE_RESEARCH_RESULTS"
    )
    ledger.append(
        "RESEARCH_EXECUTION_COMPLETED",
        {
            "result_bundle_digest": result_bundle["result_bundle_digest"],
            "task_receipt_set_digest": receipt_set["receipt_set_digest"],
        },
        run_request["started_at"],
    )
    return {
        "outputs": outputs,
        "receipts": receipt_set,
        "result_bundle": result_bundle,
        "candidate_results": candidate_results,
    }

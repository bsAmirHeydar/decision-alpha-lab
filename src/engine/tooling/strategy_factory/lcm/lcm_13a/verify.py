from __future__ import annotations
from pathlib import Path
from .canonical import verify_embedded_digest
from .io import iter_jsonl, load_json

REQUIRED = (
    "dual_run_harness/README.md",
    "dual_run_harness/harness_contract.json",
    "dual_run_harness/comparison_dimension_registry.json",
    "dual_run_harness/side_effect_fence.json",
    "dual_run_harness/replay_clock_contract.json",
    "dual_run_harness/mismatch_persistence_policy.json",
    "dual_run_scenario_registry.json",
    "mismatch_registry.jsonl",
    "mismatch_taxonomy.json",
    "variance_approval_registry.json",
    "consumer_eligibility_registry.json",
    "mismatch_frequency_registry.json",
    "dual_run_summary.md",
    "LCM13A_TO_LCM13B_HANDOFF.json",
    "dual_run_marker.json",
    "dual_run_receipt.json",
    "required_artifact_locator.json",
    "rollback_manifest.json",
    "output_manifest.json",
    "reports/acceptance_report.json",
    "reports/hostile_review_report.json",
    "records/exact_consumer_inventory.jsonl",
    "records/dual_run_scenarios.jsonl",
    "records/dual_run_results.jsonl",
    "records/consumer_eligibility_records.jsonl",
)
DIGEST_FIELDS = {
    "dual_run_harness/harness_contract.json": "contract_digest",
    "dual_run_harness/comparison_dimension_registry.json": "registry_digest",
    "dual_run_harness/side_effect_fence.json": "fence_digest",
    "dual_run_harness/replay_clock_contract.json": "clock_contract_digest",
    "dual_run_harness/mismatch_persistence_policy.json": "policy_digest",
    "dual_run_scenario_registry.json": "registry_digest",
    "mismatch_taxonomy.json": "taxonomy_digest",
    "variance_approval_registry.json": "registry_digest",
    "consumer_eligibility_registry.json": "registry_digest",
    "mismatch_frequency_registry.json": "registry_digest",
    "LCM13A_TO_LCM13B_HANDOFF.json": "handoff_digest",
    "dual_run_marker.json": "marker_digest",
    "dual_run_receipt.json": "receipt_digest",
    "required_artifact_locator.json": "locator_digest",
    "rollback_manifest.json": "rollback_digest",
    "output_manifest.json": "output_manifest_digest",
    "reports/acceptance_report.json": "report_digest",
    "reports/hostile_review_report.json": "report_digest",
}

def verify_package(root: Path) -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED:
        if not (root / relative).is_file():
            errors.append(f"MISSING:{relative}")
    for relative, field in DIGEST_FIELDS.items():
        path = root / relative
        if path.is_file() and not verify_embedded_digest(load_json(path), field):
            errors.append(f"DIGEST:{relative}")
    if errors:
        return errors
    consumers = list(iter_jsonl(root / "records/exact_consumer_inventory.jsonl"))
    scenarios = list(iter_jsonl(root / "records/dual_run_scenarios.jsonl"))
    results = list(iter_jsonl(root / "records/dual_run_results.jsonl"))
    mismatches = list(iter_jsonl(root / "mismatch_registry.jsonl"))
    eligibility = list(iter_jsonl(root / "records/consumer_eligibility_records.jsonl"))
    scenario_registry = load_json(root / "dual_run_scenario_registry.json")
    frequency = load_json(root / "mismatch_frequency_registry.json")
    variance = load_json(root / "variance_approval_registry.json")
    acceptance = load_json(root / "reports/acceptance_report.json")
    hostile = load_json(root / "reports/hostile_review_report.json")
    handoff = load_json(root / "LCM13A_TO_LCM13B_HANDOFF.json")
    fence = load_json(root / "dual_run_harness/side_effect_fence.json")
    if len(scenarios) != len(consumers) * 3:
        errors.append("SCENARIO_ACCOUNTING")
    if len(results) != len(scenarios):
        errors.append("RESULT_ACCOUNTING")
    if any(not row["input_equality"] for row in scenarios):
        errors.append("INPUT_EQUALITY")
    if any(row["legacy_input_digest"] != row["canonical_input_digest"] for row in results):
        errors.append("RESULT_INPUT_EQUALITY")
    if frequency["raw_mismatch_count"] != len(mismatches) or frequency["suppressed_mismatch_count"] != 0:
        errors.append("MISMATCH_ACCOUNTING")
    if frequency["aggregation_rule_count"] != 0 or not frequency["repeated_mismatches_retained"]:
        errors.append("MISMATCH_AGGREGATION")
    if variance["approval_count"] != 0:
        errors.append("UNEXPECTED_VARIANCE")
    eligible_ids = {r["consumer_id"] for r in eligibility if r["eligibility_state"].startswith("ELIGIBLE")}
    if any(m["consumer_id"] in eligible_ids and m["severity"] in {"HIGH", "CRITICAL"} for m in mismatches):
        errors.append("ELIGIBLE_HARD_MISMATCH")
    if not acceptance["passed"] or hostile["result"] != "PASS":
        errors.append("ACCEPTANCE")
    if scenario_registry["input_equality_failure_count"] != 0:
        errors.append("SCENARIO_INPUT_FAILURE")
    if fence["broker_submission_enabled"] or fence["live_order_enabled"] or fence["capital_activation_enabled"]:
        errors.append("SIDE_EFFECT_FENCE")
    if handoff["consumer_cutover_performed"] or handoff["runtime_authority_created"] or handoff["live_order_authority_created"] or handoff["capital_authority_created"]:
        errors.append("AUTHORITY_ESCALATION")
    return errors

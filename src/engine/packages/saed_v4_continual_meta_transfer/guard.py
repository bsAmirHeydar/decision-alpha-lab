from __future__ import annotations

from .canonical import seal, stable_id


def evaluate(task: dict, prior: dict, drift_event: dict, evaluation: dict, minimum_delta: float = -0.02) -> dict:
    reasons = []
    if prior["fallback_to_scratch"]:
        reasons.append("no_eligible_transfer_source")
    if drift_event["drift_class"] == "novel":
        reasons.append("novel_drift_segment")
    if float(task["support_score"]) < 0.5:
        reasons.append("insufficient_target_support")
    if float(task["ood_pvalue"]) < 0.05:
        reasons.append("target_ood_gate_failed")
    if float(task["conformal_value_lower_bound"]) < -0.1:
        reasons.append("target_conformal_lower_bound_failed")
    if float(evaluation["utility_delta"]) < minimum_delta:
        reasons.append("retrospective_negative_transfer")
    accepted = not reasons
    payload = {
        "task_id": task["task_id"],
        "transfer_prior_id": prior["transfer_prior_id"],
        "drift_class": drift_event["drift_class"],
        "accepted_for_research_analysis": accepted,
        "selected_path": "transfer_candidate" if accepted else "scratch_baseline",
        "reasons": reasons,
        "safe_fallback": "scratch_baseline",
        "decision_authority": False,
        "promotion_eligible": False,
        "runtime_executable": False,
    }
    payload["guard_id"] = stable_id("negative_transfer_guard", payload)
    return seal(payload, "guard_hash")

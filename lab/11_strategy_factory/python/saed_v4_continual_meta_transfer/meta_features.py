from __future__ import annotations

from .canonical import content_hash, seal, stable_id
from .numerics import mean, standard_deviation


def extract(task: dict) -> dict:
    support_targets = [float(value) for value in task["support_targets"]]
    summary = [float(value) for value in task["feature_summary"]]
    vector = summary + [
        float(task["support_score"]),
        float(task["ood_pvalue"]),
        float(task["conformal_value_lower_bound"]),
        mean(support_targets),
        standard_deviation(support_targets),
        float(len(support_targets)),
    ]
    payload = {
        "task_id": str(task["task_id"]),
        "context_id": str(task["context_id"]),
        "cluster_id": str(task["cluster_id"]),
        "regime": str(task["regime"]),
        "decision_time": str(task["decision_time"]),
        "vector": vector,
        "uses_support_outcomes": True,
        "uses_query_outcomes": False,
        "future_suffix_accessed": False,
        "protected_evidence_accessed": False,
    }
    payload["meta_feature_id"] = stable_id("meta_feature", payload)
    return seal(payload, "meta_feature_hash")


def build(tasks: list[dict]) -> list[dict]:
    return [extract(task) for task in tasks]

from __future__ import annotations

from collections import defaultdict

from .budget import ResearchLedger
from .canonical import seal, stable_id
from .contracts import ReplayContract
from .numerics import l2_distance


def build(tasks: list[dict], drift_events: list[dict], meta_features: list[dict], contract: ReplayContract, ledger: ResearchLedger) -> dict:
    event_by_task = {item["task_id"]: item for item in drift_events}
    feature_by_task = {item["task_id"]: item for item in meta_features}
    eligible = [task for task in tasks if task["role"] == "meta_train"]
    selected: list[dict] = []
    covered_contexts = set()
    covered_classes = set()
    ordered = sorted(eligible, key=lambda item: (item["decision_time"], item["task_id"]), reverse=True)
    for task in ordered:
        drift_class = event_by_task[task["task_id"]]["drift_class"]
        if task["context_id"] not in covered_contexts or drift_class not in covered_classes:
            selected.append(task)
            covered_contexts.add(task["context_id"])
            covered_classes.add(drift_class)
        if len(selected) >= contract.capacity:
            break
    while len(selected) < min(contract.capacity, len(ordered)):
        remaining = [task for task in ordered if task["task_id"] not in {item["task_id"] for item in selected}]
        if not remaining:
            break
        def diversity(task: dict) -> tuple[float, str]:
            vector = feature_by_task[task["task_id"]]["vector"]
            minimum = min((l2_distance(vector, feature_by_task[item["task_id"]]["vector"]) for item in selected), default=0.0)
            return (minimum, task["task_id"])
        selected.append(max(remaining, key=diversity))
    entries = []
    for rank, task in enumerate(selected):
        ledger.consume("replay_entries", 1, task["task_id"])
        event = event_by_task[task["task_id"]]
        entry = {
            "rank": rank,
            "task_id": task["task_id"],
            "context_id": task["context_id"],
            "drift_class": event["drift_class"],
            "decision_time": task["decision_time"],
            "support_features_hash_only": True,
            "query_outcomes_stored": False,
        }
        entry["replay_entry_id"] = stable_id("replay_entry", entry)
        entries.append(entry)
    payload = {
        "phase": "SAED_V4_25",
        "capacity": contract.capacity,
        "entry_count": len(entries),
        "entries": entries,
        "contexts_covered": sorted({item["context_id"] for item in entries}),
        "drift_classes_covered": sorted({item["drift_class"] for item in entries}),
        "protected_query_outcomes_stored": False,
        "deterministic": True,
    }
    payload["replay_buffer_id"] = stable_id("replay_buffer", payload)
    return seal(payload, "replay_buffer_hash")

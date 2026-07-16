from __future__ import annotations

from collections import defaultdict

from .canonical import content_hash, seal, stable_id
from .contracts import DriftTaxonomyContract
from .numerics import cosine_similarity, l2_distance


def _distance(left: dict, right: dict) -> float:
    return l2_distance(left["vector"], right["vector"]) / max(1.0, len(left["vector"]) ** 0.5)


def classify(previous: dict | None, current: dict, history: list[dict], contract: DriftTaxonomyContract) -> dict:
    if previous is None:
        drift_class = "novel"
        distance = None
        recurrence_similarity = None
        predecessor = None
    else:
        distance = _distance(previous, current)
        predecessor = previous["task_id"]
        prior_same_context = [item for item in history[:-1] if item["context_id"] == current["context_id"]]
        recurrence_similarity = max(
            (cosine_similarity(item["vector"], current["vector"]) for item in prior_same_context),
            default=-1.0,
        )
        if recurrence_similarity >= contract.recurrence_similarity_threshold and distance > contract.stationary_threshold:
            drift_class = "recurring"
        elif distance <= contract.stationary_threshold:
            drift_class = "stationary"
        elif distance <= contract.gradual_threshold:
            drift_class = "gradual"
        elif distance <= contract.sudden_threshold:
            drift_class = "sudden"
        else:
            drift_class = "novel"
    payload = {
        "task_id": current["task_id"],
        "context_id": current["context_id"],
        "predecessor_task_id": predecessor,
        "meta_distance": distance,
        "recurrence_similarity": recurrence_similarity,
        "drift_class": drift_class,
        "fail_closed": drift_class == "novel",
        "deterministic": True,
    }
    payload["drift_event_id"] = stable_id("drift_event", payload)
    return seal(payload, "drift_event_hash")


def segment(meta_features: list[dict], contract: DriftTaxonomyContract) -> dict:
    history: list[dict] = []
    last_by_context: dict[str, dict] = {}
    events: list[dict] = []
    for feature in meta_features:
        previous = last_by_context.get(feature["context_id"])
        history.append(feature)
        event = classify(previous, feature, history, contract)
        events.append(event)
        last_by_context[feature["context_id"]] = feature
    class_counts: dict[str, int] = defaultdict(int)
    for event in events:
        class_counts[event["drift_class"]] += 1
    segments = []
    for event in events:
        if not segments or segments[-1]["context_id"] != event["context_id"] or segments[-1]["drift_class"] != event["drift_class"]:
            segments.append({
                "segment_id": stable_id("drift_segment", {"context_id": event["context_id"], "first": event["task_id"], "class": event["drift_class"]}),
                "context_id": event["context_id"],
                "drift_class": event["drift_class"],
                "task_ids": [event["task_id"]],
            })
        else:
            segments[-1]["task_ids"].append(event["task_id"])
    payload = {
        "phase": "SAED_V4_25",
        "events": events,
        "segments": segments,
        "class_counts": dict(sorted(class_counts.items())),
        "taxonomy_hash": content_hash({"classes": list(contract.allowed_classes), "thresholds": [contract.stationary_threshold, contract.gradual_threshold, contract.sudden_threshold]}),
        "deterministic": True,
    }
    payload["drift_report_id"] = stable_id("drift_report", payload)
    return seal(payload, "drift_report_hash")

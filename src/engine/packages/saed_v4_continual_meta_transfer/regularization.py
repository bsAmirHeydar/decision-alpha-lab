from __future__ import annotations

from .canonical import seal, stable_id
from .numerics import clamp


def importance_from_support(features: list[list[float]], floor: float = 1e-6) -> list[float]:
    if not features:
        raise ValueError("support features cannot be empty")
    dimension = len(features[0])
    return [max(floor, sum(float(row[index]) ** 2 for row in features) / len(features)) for index in range(dimension)]


def anchor(adaptation: dict, task: dict, strength: float = 0.15, maximum_delta: float = 0.75) -> dict:
    baseline = [float(value) for value in adaptation["baseline_parameters"]]
    adapted = [float(value) for value in adaptation["adapted_parameters"]]
    importance = importance_from_support(task["support_features"])
    anchored = []
    penalties = []
    for baseline_value, adapted_value, importance_value in zip(baseline, adapted, importance):
        delta = adapted_value - baseline_value
        shrink = 1.0 / (1.0 + strength * importance_value)
        safe_delta = clamp(delta * shrink, -maximum_delta, maximum_delta)
        anchored.append(baseline_value + safe_delta)
        penalties.append(importance_value * safe_delta * safe_delta)
    payload = {
        "task_id": task["task_id"],
        "adaptation_id": adaptation["adaptation_id"],
        "importance_diagonal": importance,
        "anchor_strength": strength,
        "anchored_parameters": anchored,
        "quadratic_penalty": sum(penalties),
        "baseline_preserved": True,
        "runtime_mutation": False,
    }
    payload["regularization_id"] = stable_id("regularization", payload)
    return seal(payload, "regularization_hash")

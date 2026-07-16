from __future__ import annotations

import math

from .canonical import seal, stable_id
from .contracts import ContinualCalibrationContract
from .numerics import quantile


def fit_past_only(tasks: list[dict], predictions_by_task: dict[str, list[float]], contract: ContinualCalibrationContract) -> list[dict]:
    history: list[tuple[str, list[float]]] = []
    states = []
    for task in tasks:
        task_id = task["task_id"]
        residual_pool = [value for _, residuals in history[-contract.window_tasks :] for value in residuals]
        if len(residual_pool) < contract.minimum_residuals:
            threshold = None
            ready = False
        else:
            rank_probability = min(1.0, math.ceil((len(residual_pool) + 1) * (1.0 - contract.alpha)) / len(residual_pool))
            threshold = quantile(residual_pool, rank_probability)
            ready = True
        state = {
            "task_id": task_id,
            "history_task_ids": [item[0] for item in history[-contract.window_tasks :]],
            "residual_count": len(residual_pool),
            "downside_quantile": threshold,
            "ready": ready,
            "past_only": True,
            "runtime_mutation": False,
        }
        state["calibration_state_id"] = stable_id("continual_calibration", state)
        states.append(seal(state, "calibration_state_hash"))
        predictions = predictions_by_task[task_id]
        outcomes = [float(value) for value in task["query_targets"]]
        residuals = [max(0.0, predicted - outcome) for predicted, outcome in zip(predictions, outcomes)]
        history.append((task_id, residuals))
    return states

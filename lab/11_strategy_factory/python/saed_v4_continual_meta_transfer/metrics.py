from __future__ import annotations

import hashlib
import random
from collections import defaultdict

from .canonical import seal, stable_id
from .contracts import ForgettingContract
from .numerics import dot, mean, quantile


def predict(features: list[list[float]], parameters: list[float]) -> list[float]:
    return [dot(row, parameters) for row in features]


def utility(predictions: list[float], targets: list[float]) -> float:
    if len(predictions) != len(targets) or not predictions:
        raise ValueError("utility inputs are misaligned or empty")
    mse = mean((float(predicted) - float(target)) ** 2 for predicted, target in zip(predictions, targets))
    downside = mean(max(0.0, float(predicted) - float(target)) for predicted, target in zip(predictions, targets))
    return -(mse + 0.25 * downside)


def evaluate(tasks: list[dict], regularizations: list[dict]) -> list[dict]:
    regularization_by_task = {item["task_id"]: item for item in regularizations}
    evaluations = []
    for task in tasks:
        baseline_parameters = [float(value) for value in task["baseline_parameters"]]
        transfer_parameters = regularization_by_task[task["task_id"]]["anchored_parameters"]
        baseline_predictions = predict(task["query_features"], baseline_parameters)
        transfer_predictions = predict(task["query_features"], transfer_parameters)
        targets = [float(value) for value in task["query_targets"]]
        baseline_utility = utility(baseline_predictions, targets)
        transfer_utility = utility(transfer_predictions, targets)
        payload = {
            "task_id": task["task_id"],
            "context_id": task["context_id"],
            "cluster_id": task["cluster_id"],
            "role": task["role"],
            "baseline_predictions": baseline_predictions,
            "transfer_predictions": transfer_predictions,
            "baseline_utility": baseline_utility,
            "transfer_utility": transfer_utility,
            "utility_delta": transfer_utility - baseline_utility,
            "query_outcomes_used_only_for_retrospective_evaluation": True,
            "promotion_eligible": False,
        }
        payload["evaluation_id"] = stable_id("transfer_evaluation", payload)
        evaluations.append(seal(payload, "evaluation_hash"))
    return evaluations


def _cluster_bootstrap(values: list[dict], draws: int, seed_material: str) -> tuple[float, float]:
    by_cluster: dict[str, list[float]] = defaultdict(list)
    for item in values:
        by_cluster[item["cluster_id"]].append(float(item["utility_delta"]))
    clusters = sorted(by_cluster)
    if not clusters:
        return 0.0, 0.0
    seed = int(hashlib.sha256(seed_material.encode("utf-8")).hexdigest()[:16], 16)
    randomizer = random.Random(seed)
    samples = []
    for _ in range(draws):
        selected = [randomizer.choice(clusters) for _ in clusters]
        sample_values = [value for cluster in selected for value in by_cluster[cluster]]
        samples.append(mean(sample_values))
    return quantile(samples, 0.025), quantile(samples, 0.975)


def transfer_report(evaluations: list[dict], contract: ForgettingContract) -> dict:
    validation = [item for item in evaluations if item["role"] == "meta_validation"]
    transfer_test = [item for item in evaluations if item["role"] == "transfer_test"]
    meta_train = [item for item in evaluations if item["role"] == "meta_train"]
    forward = mean(item["utility_delta"] for item in transfer_test)
    backward = mean(item["utility_delta"] for item in meta_train)
    mean_forgetting = max(0.0, -backward)
    worst_task_forgetting = max([max(0.0, -float(item["utility_delta"])) for item in meta_train] or [0.0])
    lower, upper = _cluster_bootstrap(transfer_test, contract.bootstrap_draws, "SAED_V4_25_FORWARD_TRANSFER")
    negative_count = sum(float(item["utility_delta"]) < 0 for item in evaluations)
    payload = {
        "phase": "SAED_V4_25",
        "evaluation_count": len(evaluations),
        "forward_transfer": forward,
        "forward_transfer_ci_lower": lower,
        "forward_transfer_ci_upper": upper,
        "backward_transfer": backward,
        "mean_forgetting": mean_forgetting,
        "worst_task_forgetting": worst_task_forgetting,
        "negative_transfer_count": negative_count,
        "meta_validation_mean_delta": mean(item["utility_delta"] for item in validation),
        "gates": {
            "forward_transfer": lower >= contract.minimum_forward_transfer,
            "backward_transfer": backward >= contract.minimum_backward_transfer,
            "mean_forgetting": mean_forgetting <= contract.maximum_mean_forgetting,
            "worst_task_forgetting": worst_task_forgetting <= contract.maximum_worst_task_forgetting,
        },
        "cluster_bootstrap": True,
        "bootstrap_draws": contract.bootstrap_draws,
        "confidence_level": contract.confidence_level,
    }
    payload["accepted_for_transfer_research"] = all(payload["gates"].values())
    payload["transfer_report_id"] = stable_id("transfer_report", payload)
    return seal(payload, "transfer_report_hash")

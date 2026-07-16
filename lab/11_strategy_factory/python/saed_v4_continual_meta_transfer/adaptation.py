from __future__ import annotations

from .budget import ResearchLedger
from .canonical import seal, stable_id
from .contracts import AdaptationContract
from .numerics import clamp


def _fit_linear(features: list[list[float]], targets: list[float], ridge: float, dimension: int) -> list[float]:
    # Deterministic coordinate-wise diagonal ridge approximation. It is intentionally
    # transparent and dependency-free; challengers may use full solvers behind the same contract.
    if len(features) != len(targets):
        raise ValueError("support feature/target mismatch")
    parameters = []
    for column in range(dimension):
        numerator = sum(float(row[column]) * float(target) for row, target in zip(features, targets))
        denominator = sum(float(row[column]) ** 2 for row in features) + ridge
        parameters.append(numerator / denominator if denominator > 0 else 0.0)
    return parameters


def adapt(target: dict, prior: dict, contract: AdaptationContract, ledger: ResearchLedger) -> dict:
    ledger.consume("adaptations", 1, target["task_id"])
    features = [[float(value) for value in row] for row in target["support_features"]]
    targets = [float(value) for value in target["support_targets"]]
    baseline = [float(value) for value in target["baseline_parameters"]]
    prior_parameters = [float(value) for value in prior["prior_parameters"]]
    if len(features) < contract.minimum_support_rows:
        chosen = baseline
        support_fit = baseline
        fallback = True
    else:
        support_fit = _fit_linear(features, targets, contract.ridge_penalty, len(baseline))
        strength = contract.prior_strength
        sample = float(len(features))
        blended = [
            (sample * empirical + strength * prior_value) / (sample + strength)
            for empirical, prior_value in zip(support_fit, prior_parameters)
        ]
        chosen = [
            baseline_value + clamp(candidate - baseline_value, -contract.maximum_parameter_delta, contract.maximum_parameter_delta)
            for baseline_value, candidate in zip(baseline, blended)
        ]
        fallback = False
    payload = {
        "task_id": target["task_id"],
        "prior_id": prior["transfer_prior_id"],
        "baseline_parameters": baseline,
        "support_fit_parameters": support_fit,
        "adapted_parameters": chosen,
        "support_rows": len(features),
        "fallback_to_baseline": fallback,
        "query_outcomes_accessed": False,
        "promotion_eligible": False,
        "runtime_executable": False,
    }
    payload["adaptation_id"] = stable_id("adaptation", payload)
    return seal(payload, "adaptation_hash")

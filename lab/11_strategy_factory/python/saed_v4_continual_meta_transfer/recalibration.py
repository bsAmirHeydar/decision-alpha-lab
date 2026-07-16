from __future__ import annotations

import itertools

from .budget import ResearchLedger
from .canonical import seal, stable_id
from .contracts import RecalibrationExperimentContract
from .numerics import mean


def run(evaluations: list[dict], contract: RecalibrationExperimentContract, ledger: ResearchLedger) -> dict:
    validation = [item for item in evaluations if item["role"] == contract.selection_role]
    trials = []
    for window, prior_strength, ridge in itertools.product(
        contract.candidate_window_grid,
        contract.candidate_prior_strength_grid,
        contract.candidate_ridge_grid,
    ):
        ledger.consume("recalibration_trials", 1, f"w={window},p={prior_strength},r={ridge}")
        # Reference objective is intentionally deterministic and audit-friendly. It uses
        # only the frozen meta-validation evaluations and an explicit complexity penalty.
        base = mean(item["utility_delta"] for item in validation)
        stability = 1.0 / (1.0 + abs(window - 4) + abs(prior_strength - 4.0) + abs(ridge - 0.2))
        complexity_penalty = 0.0005 * window + 0.0002 * prior_strength + 0.0001 / max(ridge, 1e-9)
        objective = base + 0.01 * stability - complexity_penalty
        payload = {
            "window_tasks": window,
            "prior_strength": prior_strength,
            "ridge_penalty": ridge,
            "objective": objective,
            "validation_records": len(validation),
            "hidden_evaluation_queries": 0,
            "online_mutation": False,
            "promotion_eligible": False,
        }
        payload["trial_id"] = stable_id("recalibration_trial", payload)
        trials.append(payload)
    trials.sort(key=lambda item: (-item["objective"], item["window_tasks"], item["prior_strength"], item["ridge_penalty"], item["trial_id"]))
    selected = trials[0] if trials else None
    payload = {
        "phase": "SAED_V4_25",
        "trial_count": len(trials),
        "trials": trials,
        "selected_research_configuration": selected,
        "selection_role": contract.selection_role,
        "hidden_evaluation_queries": 0,
        "online_policy_mutations": 0,
        "runtime_compilations": 0,
        "order_submissions": 0,
        "deterministic": True,
    }
    payload["experiment_id"] = stable_id("safe_recalibration_experiment", payload)
    return seal(payload, "experiment_hash")

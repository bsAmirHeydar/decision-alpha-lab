from __future__ import annotations

import copy

from saed_v4_continual_meta_transfer.continual import fit_past_only
from saed_v4_continual_meta_transfer.contracts import ContinualCalibrationContract
from saed_v4_continual_meta_transfer.guard import evaluate


def _predictions(tasks):
    return {task["task_id"]: [0.0] * len(task["query_targets"]) for task in tasks}


def test_current_outcome_mutation_does_not_change_current_calibration_state(config, tasks):
    contract = ContinualCalibrationContract.from_mapping(config["continual_calibration_contract"])
    first = fit_past_only(tasks, _predictions(tasks), contract)
    mutated = copy.deepcopy(tasks)
    mutated[20]["query_targets"] = [value + 100 for value in mutated[20]["query_targets"]]
    second = fit_past_only(mutated, _predictions(mutated), contract)
    assert first[20] == second[20]
    assert first[21] != second[21]


def test_calibration_is_past_only(config, tasks):
    states = fit_past_only(tasks, _predictions(tasks), ContinualCalibrationContract.from_mapping(config["continual_calibration_contract"]))
    assert all(state["past_only"] and state["runtime_mutation"] is False for state in states)
    assert states[0]["ready"] is False
    assert any(state["ready"] for state in states)


def test_guard_fails_closed_for_novel_drift(tasks):
    task = tasks[20]
    prior = {"transfer_prior_id":"p","fallback_to_scratch":False}
    drift = {"drift_class":"novel"}
    evaluation = {"utility_delta":0.1}
    result = evaluate(task, prior, drift, evaluation)
    assert not result["accepted_for_research_analysis"]
    assert result["selected_path"] == "scratch_baseline"


def test_guard_fails_closed_for_low_ood(tasks):
    task = copy.deepcopy(tasks[20])
    task["ood_pvalue"] = 0.001
    result = evaluate(task, {"transfer_prior_id":"p","fallback_to_scratch":False}, {"drift_class":"stationary"}, {"utility_delta":0.1})
    assert "target_ood_gate_failed" in result["reasons"]


def test_guard_never_grants_authority(tasks):
    task = tasks[20]
    result = evaluate(task, {"transfer_prior_id":"p","fallback_to_scratch":False}, {"drift_class":"stationary"}, {"utility_delta":0.1})
    assert result["decision_authority"] is False
    assert result["promotion_eligible"] is False
    assert result["runtime_executable"] is False

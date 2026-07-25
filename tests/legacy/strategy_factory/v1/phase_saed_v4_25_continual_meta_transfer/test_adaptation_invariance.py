from __future__ import annotations

import copy

from saed_v4_continual_meta_transfer.adaptation import adapt
from saed_v4_continual_meta_transfer.budget import ResearchLedger
from saed_v4_continual_meta_transfer.contracts import AdaptationContract, ResearchBudget
from saed_v4_continual_meta_transfer.regularization import anchor


def _ledger(config):
    return ResearchLedger(ResearchBudget.from_mapping(config["research_budget"]))


def test_query_outcome_mutation_does_not_change_adaptation(config, tasks):
    task = copy.deepcopy(tasks[20])
    prior = {
        "transfer_prior_id": "transfer_prior_test",
        "prior_parameters": list(task["baseline_parameters"]),
    }
    contract = AdaptationContract.from_mapping(config["adaptation_contract"])
    first = adapt(task, prior, contract, _ledger(config))
    task["query_targets"] = [value + 1000 for value in task["query_targets"]]
    second = adapt(task, prior, contract, _ledger(config))
    assert first == second


def test_support_outcome_mutation_changes_adaptation(config, tasks):
    task = copy.deepcopy(tasks[20])
    prior = {"transfer_prior_id": "transfer_prior_test", "prior_parameters": list(task["baseline_parameters"])}
    contract = AdaptationContract.from_mapping(config["adaptation_contract"])
    first = adapt(task, prior, contract, _ledger(config))
    task["support_targets"][0] += 1.0
    second = adapt(task, prior, contract, _ledger(config))
    assert first["adapted_parameters"] != second["adapted_parameters"]


def test_regularization_preserves_baseline_and_bounds_delta(config, tasks):
    task = tasks[20]
    prior = {"transfer_prior_id": "transfer_prior_test", "prior_parameters": [10.0] * 6}
    adaptation = adapt(task, prior, AdaptationContract.from_mapping(config["adaptation_contract"]), _ledger(config))
    result = anchor(adaptation, task, maximum_delta=0.75)
    assert result["baseline_preserved"]
    assert all(abs(a-b) <= 0.7500000001 for a,b in zip(result["anchored_parameters"], adaptation["baseline_parameters"]))


def test_adaptation_never_claims_runtime(config, tasks):
    task = tasks[25]
    prior = {"transfer_prior_id": "transfer_prior_test", "prior_parameters": list(task["baseline_parameters"])}
    result = adapt(task, prior, AdaptationContract.from_mapping(config["adaptation_contract"]), _ledger(config))
    assert result["promotion_eligible"] is False
    assert result["runtime_executable"] is False

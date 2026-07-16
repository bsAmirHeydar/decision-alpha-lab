from __future__ import annotations

import copy

import pytest

from saed_v4_continual_meta_transfer.budget import ResearchLedger
from saed_v4_continual_meta_transfer.contracts import MetaDatasetContract, ResearchBudget
from saed_v4_continual_meta_transfer.dataset import validate
from saed_v4_continual_meta_transfer.errors import ContractError, KnownTimeError


def _ledger(config):
    return ResearchLedger(ResearchBudget.from_mapping(config["research_budget"]))


def test_golden_dataset_validates(config, tasks):
    result = validate(tasks, MetaDatasetContract.from_mapping(config["meta_dataset_contract"]), _ledger(config))
    assert result["task_count"] == 48
    assert result["context_count"] == 4
    assert result["future_suffix_queries"] == 0


@pytest.mark.parametrize("field", ["future_suffix_accessed", "protected_evidence_accessed"])
def test_forbidden_evidence_flags_fail(config, tasks, field):
    mutated = copy.deepcopy(tasks)
    mutated[0][field] = True
    with pytest.raises(KnownTimeError):
        validate(mutated, MetaDatasetContract.from_mapping(config["meta_dataset_contract"]), _ledger(config))


@pytest.mark.parametrize("field,value", [
    ("feature_known_at", "2027-01-01T00:00:00Z"),
    ("decision_time", "2023-01-01T00:00:00Z"),
    ("outcome_observed_at", "2023-01-01T00:00:00Z"),
])
def test_time_ordering_fails(config, tasks, field, value):
    mutated = copy.deepcopy(tasks)
    mutated[0][field] = value
    with pytest.raises(KnownTimeError):
        validate(mutated, MetaDatasetContract.from_mapping(config["meta_dataset_contract"]), _ledger(config))


def test_duplicate_task_id_fails(config, tasks):
    mutated = copy.deepcopy(tasks)
    mutated[1]["task_id"] = mutated[0]["task_id"]
    with pytest.raises(ContractError):
        validate(mutated, MetaDatasetContract.from_mapping(config["meta_dataset_contract"]), _ledger(config))


def test_cluster_role_overlap_fails(config, tasks):
    mutated = copy.deepcopy(tasks)
    mutated[20]["cluster_id"] = mutated[0]["cluster_id"]
    with pytest.raises(ContractError):
        validate(mutated, MetaDatasetContract.from_mapping(config["meta_dataset_contract"]), _ledger(config))


@pytest.mark.parametrize("index", range(0, 48, 4))
def test_each_context_task_dimension_is_frozen(config, tasks, index):
    task = tasks[index]
    assert len(task["feature_summary"]) == len(config["meta_dataset_contract"]["feature_names"])
    assert len(task["baseline_parameters"]) == len(config["meta_dataset_contract"]["parameter_names"])

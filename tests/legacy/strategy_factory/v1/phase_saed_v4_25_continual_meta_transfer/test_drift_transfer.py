from __future__ import annotations

import pytest

from saed_v4_continual_meta_transfer.budget import ResearchLedger
from saed_v4_continual_meta_transfer.contracts import DriftTaxonomyContract, ResearchBudget, TransferContract
from saed_v4_continual_meta_transfer.drift import segment
from saed_v4_continual_meta_transfer.meta_features import build
from saed_v4_continual_meta_transfer.transfer import map_transfers


def test_drift_segmentation_deterministic(config, tasks):
    features = build(tasks)
    contract = DriftTaxonomyContract.from_mapping(config["drift_taxonomy_contract"])
    assert segment(features, contract) == segment(features, contract)


def test_first_context_observation_is_novel(config, tasks):
    report = segment(build(tasks), DriftTaxonomyContract.from_mapping(config["drift_taxonomy_contract"]))
    first_by_context = {}
    for event in report["events"]:
        first_by_context.setdefault(event["context_id"], event)
    assert all(event["drift_class"] == "novel" for event in first_by_context.values())


def test_transfer_map_never_uses_future_sources(config, tasks):
    features = build(tasks)
    ledger = ResearchLedger(ResearchBudget.from_mapping(config["research_budget"]))
    result = map_transfers(tasks, tasks[:12], features, TransferContract.from_mapping(config["transfer_contract"]), ledger)
    by_id = {task["task_id"]: task for task in tasks}
    assert all(by_id[edge["source_task_id"]]["decision_time"] < by_id[edge["target_task_id"]]["decision_time"] for edge in result["edges"])


def test_transfer_map_never_uses_same_cluster(config, tasks):
    features = build(tasks)
    ledger = ResearchLedger(ResearchBudget.from_mapping(config["research_budget"]))
    result = map_transfers(tasks, tasks[:12], features, TransferContract.from_mapping(config["transfer_contract"]), ledger)
    by_id = {task["task_id"]: task for task in tasks}
    assert all(by_id[edge["source_task_id"]]["cluster_id"] != by_id[edge["target_task_id"]]["cluster_id"] for edge in result["edges"])


@pytest.mark.parametrize("target_index", range(12))
def test_early_meta_train_tasks_fail_closed_when_no_prior_source(config, tasks, target_index):
    features = build(tasks)
    ledger = ResearchLedger(ResearchBudget.from_mapping(config["research_budget"]))
    result = map_transfers(tasks, tasks[:12], features, TransferContract.from_mapping(config["transfer_contract"]), ledger)
    prior = result["priors"][target_index]
    if target_index == 0:
        assert prior["fallback_to_scratch"]
    assert prior["source_query_outcomes_accessed"] is False

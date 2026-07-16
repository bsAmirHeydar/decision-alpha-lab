from __future__ import annotations

import pytest

from saed_v4_continual_meta_transfer.budget import ResearchLedger
from saed_v4_continual_meta_transfer.canonical import content_hash, stable_id
from saed_v4_continual_meta_transfer.contracts import ResearchBudget
from saed_v4_continual_meta_transfer.errors import BudgetError


def test_canonical_hash_is_order_invariant():
    assert content_hash({"b":2,"a":1}) == content_hash({"a":1,"b":2})


def test_stable_id_is_deterministic():
    assert stable_id("task", {"x":1}) == stable_id("task", {"x":1})


def test_nonfinite_hash_rejected():
    with pytest.raises(ValueError):
        content_hash({"x": float("nan")})


def test_budget_snapshot_is_complete(config):
    ledger = ResearchLedger(ResearchBudget.from_mapping(config["research_budget"]))
    ledger.consume("tasks", 1, "test")
    snapshot = ledger.snapshot()
    assert snapshot["complete"] and snapshot["within_budget"]


@pytest.mark.parametrize("counter", [
    "hidden_evaluation_queries","protected_evidence_exposures","runtime_compilations","order_submissions","online_policy_mutations"
])
def test_zero_authority_budgets_fail_on_first_use(config, counter):
    ledger = ResearchLedger(ResearchBudget.from_mapping(config["research_budget"]))
    with pytest.raises(BudgetError):
        ledger.consume(counter, 1, "forbidden")

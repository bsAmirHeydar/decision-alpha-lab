from dataclasses import replace
import pytest
from strategy_factory_qualification_v3.chaos import evaluate_chaos
from strategy_factory_qualification_v3.soak import evaluate_soak
from strategy_factory_qualification_v3.enums import EvidenceStatus
from strategy_factory_qualification_v3.golden import NOW, chaos_report, policy, soak_report


def test_soak_passes_budget():
    assert evaluate_soak(soak_report(), policy(), NOW).status is EvidenceStatus.PASS


@pytest.mark.parametrize("field,value,reason", [
    ("duration_minutes", 1, "soak_duration_below_minimum"),
    ("processed_events", 1, "soak_events_below_minimum"),
    ("critical_errors", 1, "critical_error"),
    ("unhandled_exceptions", 1, "unhandled_exception"),
    ("reconciliation_mismatches", 1, "reconciliation_mismatch"),
    ("duplicate_actions", 1, "duplicate_action"),
    ("stale_actions", 1, "stale_action"),
    ("max_memory_growth_mb", 1000.0, "memory_growth_budget"),
    ("p99_latency_ms", 1000.0, "latency_budget"),
])
def test_soak_failures_are_non_compensatory(field, value, reason):
    report = replace(soak_report(), **{field: value})
    result = evaluate_soak(report, policy(), NOW)
    assert result.status is EvidenceStatus.FAIL and reason in result.reason_codes


def test_chaos_passes_required_matrix():
    assert evaluate_chaos(chaos_report(), policy(), NOW).status is EvidenceStatus.PASS


def test_chaos_recovery_failure_is_blocking():
    assert evaluate_chaos(chaos_report(False), policy(), NOW).status is EvidenceStatus.FAIL


def test_missing_chaos_scenario_is_blocking():
    report = replace(chaos_report(), scenarios=chaos_report().scenarios[:-1])
    result = evaluate_chaos(report, policy(), NOW)
    assert any(x.startswith("missing_chaos_scenario") for x in result.reason_codes)

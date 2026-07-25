from dataclasses import replace
import pytest
from strategy_factory_qualification_v3.compile_evidence import evaluate_compile
from strategy_factory_qualification_v3.differential import evaluate_differential
from strategy_factory_qualification_v3.enums import EvidenceStatus, GateName
from strategy_factory_qualification_v3.golden import NOW, compile_evidence, differential_report, policy


def test_compile_passes_all_required_targets():
    assert evaluate_compile(compile_evidence(), policy(), NOW).status is EvidenceStatus.PASS


def test_compile_failure_is_blocking():
    result = evaluate_compile(compile_evidence(False), policy(), NOW)
    assert result.status is EvidenceStatus.FAIL and any("compile_failed" in x for x in result.reason_codes)


def test_missing_compile_target_is_blocking():
    evidence = replace(compile_evidence(), targets=compile_evidence().targets[:1])
    assert "missing_compile_target:diagnostic" in evaluate_compile(evidence, policy(), NOW).reason_codes


def test_compile_warning_budget_is_enforced():
    first = replace(compile_evidence().targets[0], warnings=1)
    evidence = replace(compile_evidence(), targets=(first,) + compile_evidence().targets[1:])
    assert any("compile_warning_budget" in x for x in evaluate_compile(evidence, policy(), NOW).reason_codes)


def test_differential_passes_golden_cases():
    assert evaluate_differential(differential_report(), policy(), NOW).status is EvidenceStatus.PASS


def test_differential_mismatch_is_blocking():
    assert evaluate_differential(differential_report(False), policy(), NOW).status is EvidenceStatus.FAIL


def test_future_read_is_blocking():
    report = replace(differential_report(), future_read_count=1)
    assert "future_read_detected" in evaluate_differential(report, policy(), NOW).reason_codes


def test_event_reordering_is_blocking():
    report = replace(differential_report(), reordered_event_count=1)
    assert "event_order_violation" in evaluate_differential(report, policy(), NOW).reason_codes


def test_declared_missing_case_is_blocking():
    report = replace(differential_report(), missing_case_ids=("risk",))
    assert "declared_missing_case:risk" in evaluate_differential(report, policy(), NOW).reason_codes


@pytest.mark.parametrize("gate", [GateName.CROSS_LANGUAGE_PARITY, GateName.TESTER_DIFFERENTIAL])
def test_differential_gate_identity_is_explicit(gate):
    assert evaluate_differential(differential_report(), policy(), NOW, gate).gate is gate

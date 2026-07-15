from dataclasses import replace
import pytest
from strategy_factory_qualification_v3.enums import EvidenceStatus
from strategy_factory_qualification_v3.golden import NOW, H3, policy, recovery_report, rollback_report, security_report
from strategy_factory_qualification_v3.recovery import evaluate_recovery, evaluate_rollback
from strategy_factory_qualification_v3.security import evaluate_security


def test_recovery_passes_exact_ledger():
    assert evaluate_recovery(recovery_report(), policy(), NOW).status is EvidenceStatus.PASS


@pytest.mark.parametrize("field,value,reason", [
    ("observed_ledger_hash", H3, "reservation_ledger_mismatch"),
    ("duplicate_action_count", 1, "duplicate_action"),
    ("unreserved_action_count", 1, "unreserved_action"),
    ("state_divergence_count", 1, "state_divergence"),
    ("rto_seconds", 1000.0, "rto_budget"),
    ("rpo_seconds", 1000.0, "rpo_budget"),
    ("kill_switch_verified", False, "kill_switch_unverified"),
    ("rollback_verified", False, "rollback_unverified"),
])
def test_recovery_failures_block(field, value, reason):
    result = evaluate_recovery(replace(recovery_report(), **{field: value}), policy(), NOW)
    assert reason in result.reason_codes


def test_rollback_passes():
    assert evaluate_rollback(rollback_report(), NOW).status is EvidenceStatus.PASS


def test_rollback_failure_blocks():
    result = evaluate_rollback(rollback_report(False), NOW)
    assert result.status is EvidenceStatus.FAIL and len(result.reason_codes) == 3


def test_security_passes_required_controls():
    assert evaluate_security(security_report(), policy(), NOW).status is EvidenceStatus.PASS


@pytest.mark.parametrize("field,value,reason", [
    ("plaintext_secret_findings", 1, "plaintext_secret_finding"),
    ("unsigned_artifacts", 1, "unsigned_artifact"),
    ("hash_mismatches", 1, "artifact_hash_mismatch"),
    ("backup_restore_verified", False, "backup_restore_unverified"),
    ("retention_policy_verified", False, "retention_policy_unverified"),
])
def test_security_failures_block(field, value, reason):
    result = evaluate_security(replace(security_report(), **{field: value}), policy(), NOW)
    assert reason in result.reason_codes

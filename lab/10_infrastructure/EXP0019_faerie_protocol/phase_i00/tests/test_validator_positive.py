from fp_i00_governance.validator import GovernanceValidator
from conftest import REPO_ROOT, load_policy


def test_repository_governance_gate_passes():
    report = GovernanceValidator(REPO_ROOT, load_policy()).run()
    assert report.passed, [issue.code for issue in report.issues]
    assert not report.errors
    assert report.checks_run >= 80


def test_report_hash_and_health_are_stable():
    first = GovernanceValidator(REPO_ROOT, load_policy()).run()
    second = GovernanceValidator(REPO_ROOT, load_policy()).run()
    assert first.evidence_hash == second.evidence_hash
    assert first.health.value == "READY"

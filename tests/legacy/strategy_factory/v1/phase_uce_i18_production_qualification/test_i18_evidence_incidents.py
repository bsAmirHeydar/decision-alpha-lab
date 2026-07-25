from strategy_factory_qualification_v3.evidence import build_evidence_bundle
from strategy_factory_qualification_v3.incidents import incident_gate_reasons
from strategy_factory_qualification_v3.contracts import IncidentRecord
from strategy_factory_qualification_v3.enums import IncidentSeverity
from strategy_factory_qualification_v3.golden import H, NOW
from strategy_factory_qualification_v3.qualification import qualify
from strategy_factory_qualification_v3.golden import *

def all_pass_report():
    return qualify(policy=policy(), environment=environment(), source_commit="abc123", evaluated_at_ms=NOW, compile_evidence=compile_evidence(), parity_report=differential_report(), tester_report=differential_report(source="tester", target="runtime"), soak_report=soak_report(), chaos_report=chaos_report(), recovery_report=recovery_report(), security_report=security_report(), paper_evidence=stage_evidence(ReleaseStage.PAPER), shadow_evidence=stage_evidence(ReleaseStage.SHADOW), micro_live_evidence=stage_evidence(ReleaseStage.MICRO_LIVE), rollback_report=rollback_report(), source_integrity_passed=True, source_integrity_evidence_hash=H, broker_reconciliation_passed=True, broker_reconciliation_evidence_hash=H2, human_approval_id="approval-1", human_approval_evidence_hash=H3)


def test_evidence_bundle_identity_is_stable():
    report = all_pass_report()
    a = build_evidence_bundle(report, {"b": H, "a": H}, True)
    b = build_evidence_bundle(report, {"a": H, "b": H}, True)
    assert a == b


def test_critical_incident_is_a_reason():
    item = IncidentRecord("inc-1", IncidentSeverity.CRITICAL, 1, 2, 3, "root", "fix", H)
    assert incident_gate_reasons((item,)) == ("critical_incident:inc-1",)


def test_incomplete_noncritical_incident_is_a_reason():
    item = IncidentRecord("inc-2", IncidentSeverity.WARNING, 1, 2, 3, "", "", H)
    assert incident_gate_reasons((item,)) == ("incomplete_incident_record:inc-2",)

from dataclasses import replace
import pytest
from strategy_factory_qualification_v3.contracts import ArtifactRef
from strategy_factory_qualification_v3.enums import EvidenceStatus, QualificationDecision, ReleaseStage
from strategy_factory_qualification_v3.errors import QualificationError
from strategy_factory_qualification_v3.golden import *
from strategy_factory_qualification_v3.qualification import qualify
from strategy_factory_qualification_v3.release import compile_release_manifest


def all_pass_report():
    return qualify(
        policy=policy(), environment=environment(), source_commit="abc123", evaluated_at_ms=NOW,
        compile_evidence=compile_evidence(), parity_report=differential_report(),
        tester_report=differential_report(source="tester", target="runtime"), soak_report=soak_report(),
        chaos_report=chaos_report(), recovery_report=recovery_report(), security_report=security_report(),
        paper_evidence=stage_evidence(ReleaseStage.PAPER), shadow_evidence=stage_evidence(ReleaseStage.SHADOW), micro_live_evidence=stage_evidence(ReleaseStage.MICRO_LIVE),
        rollback_report=rollback_report(), source_integrity_passed=True, source_integrity_evidence_hash=H, broker_reconciliation_passed=True, broker_reconciliation_evidence_hash=H2,
        human_approval_id="approval-1", human_approval_evidence_hash=H3,
    )


def test_missing_external_evidence_is_fail_closed():
    report = qualify(policy=policy(), environment=environment(), source_commit="abc", evaluated_at_ms=NOW)
    assert report.decision is QualificationDecision.BLOCKED
    assert not report.activation_allowed
    assert report.maximum_stage is ReleaseStage.BLOCKED


def test_all_required_evidence_qualifies_only_micro_live():
    report = all_pass_report()
    assert report.decision is QualificationDecision.QUALIFIED
    assert report.activation_allowed
    assert report.maximum_stage is ReleaseStage.MICRO_LIVE


def test_gate_order_is_deterministic():
    a, b = all_pass_report(), all_pass_report()
    assert a.gates == b.gates and a.report_hash == b.report_hash


def test_compile_failure_blocks_whole_report():
    report = qualify(policy=policy(), environment=environment(), source_commit="abc", evaluated_at_ms=NOW, compile_evidence=compile_evidence(False))
    assert report.decision is QualificationDecision.BLOCKED


def test_release_cannot_be_compiled_from_blocked_report():
    report = qualify(policy=policy(), environment=environment(), source_commit="abc", evaluated_at_ms=NOW)
    with pytest.raises(QualificationError):
        compile_release_manifest(report, "1.0.0", H, H2, "owner", NOW, NOW + 1000, (), ReleaseStage.PAPER, 0)


def test_release_manifest_is_bounded_to_qualified_stage():
    report = all_pass_report()
    manifest = compile_release_manifest(report, "1.0.0", H, H2, "owner", NOW, NOW + 1000, (ArtifactRef("a", "1.0.0", H3, "artifact.json", NOW),), ReleaseStage.MICRO_LIVE, 0.25)
    assert manifest.authority_order and manifest.max_risk_units == 0.25


def test_release_stage_escalation_is_rejected():
    with pytest.raises(QualificationError):
        compile_release_manifest(all_pass_report(), "1.0.0", H, H2, "owner", NOW, NOW + 1000, (), ReleaseStage.PRODUCTION, 1)


def test_shadow_release_has_no_authority():
    manifest = compile_release_manifest(all_pass_report(), "1.0.0", H, H2, "owner", NOW, NOW + 1000, (), ReleaseStage.SHADOW, 99)
    assert not manifest.authority_order and not manifest.authority_broker and manifest.max_risk_units == 0


def test_integrity_claim_without_evidence_hash_is_blocked():
    report = qualify(policy=policy(), environment=environment(), source_commit="abc", evaluated_at_ms=NOW, source_integrity_passed=True)
    assert "source_integrity_evidence_hash_missing" in report.blocking_reasons


def test_environment_mismatch_blocks_compile_gate():
    evidence = replace(compile_evidence(), environment_hash=H3)
    report = qualify(policy=policy(), environment=environment(), source_commit="abc", evaluated_at_ms=NOW, compile_evidence=evidence)
    assert "compile_environment_mismatch" in report.blocking_reasons


def test_full_stage_chain_can_qualify_production():
    report = qualify(
        policy=policy(), environment=environment(), source_commit="abc-prod", evaluated_at_ms=NOW,
        requested_stage=ReleaseStage.PRODUCTION, compile_evidence=compile_evidence(),
        parity_report=differential_report(), tester_report=differential_report(source="tester", target="runtime"),
        soak_report=soak_report(), chaos_report=chaos_report(), recovery_report=recovery_report(),
        security_report=security_report(), paper_evidence=stage_evidence(ReleaseStage.PAPER),
        shadow_evidence=stage_evidence(ReleaseStage.SHADOW), micro_live_evidence=stage_evidence(ReleaseStage.MICRO_LIVE),
        limited_live_evidence=stage_evidence(ReleaseStage.LIMITED_LIVE), production_evidence=stage_evidence(ReleaseStage.PRODUCTION),
        rollback_report=rollback_report(), source_integrity_passed=True, source_integrity_evidence_hash=H,
        broker_reconciliation_passed=True, broker_reconciliation_evidence_hash=H2,
        human_approval_id="approval-prod", human_approval_evidence_hash=H3,
    )
    assert report.decision is QualificationDecision.QUALIFIED
    assert report.maximum_stage is ReleaseStage.PRODUCTION
    assert report.activation_allowed


def test_paper_qualification_can_compile_zero_authority_manifest():
    report = qualify(
        policy=policy(), environment=environment(), source_commit="abc-paper", evaluated_at_ms=NOW,
        requested_stage=ReleaseStage.PAPER, compile_evidence=compile_evidence(), parity_report=differential_report(),
        tester_report=differential_report(source="tester", target="runtime"), soak_report=soak_report(),
        chaos_report=chaos_report(), recovery_report=recovery_report(), security_report=security_report(),
        paper_evidence=stage_evidence(ReleaseStage.PAPER), rollback_report=rollback_report(),
        source_integrity_passed=True, source_integrity_evidence_hash=H,
        broker_reconciliation_passed=True, broker_reconciliation_evidence_hash=H2,
    )
    assert report.decision is QualificationDecision.QUALIFIED and not report.activation_allowed
    manifest = compile_release_manifest(report, "1.0.0-paper", H, H2, "owner", NOW, NOW + 1000, (), ReleaseStage.PAPER, 0)
    assert not manifest.authority_order and manifest.stage is ReleaseStage.PAPER


def test_release_risk_cannot_exceed_qualification_cap():
    with pytest.raises(QualificationError):
        compile_release_manifest(all_pass_report(), "1.0.0", H, H2, "owner", NOW, NOW + 1000, (), ReleaseStage.MICRO_LIVE, 0.26)

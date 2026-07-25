from __future__ import annotations
from dataclasses import asdict
from .evidence import build_evidence_bundle
from .golden import *
from .qualification import qualify


def run_conformance(include_external_evidence: bool = False) -> dict:
    kwargs = {}
    if include_external_evidence:
        kwargs.update(
            compile_evidence=compile_evidence(),
            parity_report=differential_report(),
            tester_report=differential_report(source="tester", target="runtime"),
            soak_report=soak_report(),
            chaos_report=chaos_report(),
            recovery_report=recovery_report(),
            security_report=security_report(),
            paper_evidence=stage_evidence(ReleaseStage.PAPER),
            shadow_evidence=stage_evidence(ReleaseStage.SHADOW),
            micro_live_evidence=stage_evidence(ReleaseStage.MICRO_LIVE),
            rollback_report=rollback_report(),
            source_integrity_passed=True,
            source_integrity_evidence_hash=H,
            broker_reconciliation_passed=True,
            broker_reconciliation_evidence_hash=H2,
            human_approval_id="approval-1",
            human_approval_evidence_hash=H3,
        )
    report = qualify(
        policy=policy(), environment=environment(), source_commit="synthetic-reference", evaluated_at_ms=NOW,
        limitations=("synthetic_fixture_only", "metaeditor_compile_pending_local_windows", "broker_runtime_evidence_not_embedded"),
        **kwargs,
    )
    artifacts = {
        "environment": environment().fingerprint_hash,
        "policy": policy().policy_hash,
        "qualification_report": report.report_hash,
    }
    return {"report": asdict(report), "bundle": build_evidence_bundle(report, artifacts, include_external_evidence)}

from __future__ import annotations
from typing import Tuple
from .contracts import ArtifactRef, QualificationReport, ReleaseManifest
from .enums import QualificationDecision, ReleaseStage
from .errors import QualificationError


def compile_release_manifest(
    report: QualificationReport,
    release_version: str,
    generation_hash: str,
    rollback_generation_hash: str,
    approved_by: str,
    approved_at_ms: int,
    expires_at_ms: int,
    artifact_refs: Tuple[ArtifactRef, ...],
    requested_stage: ReleaseStage,
    max_risk_units: float,
) -> ReleaseManifest:
    if report.decision is not QualificationDecision.QUALIFIED:
        raise QualificationError("qualification_blocked", "release manifest cannot be compiled from a blocked or incomplete report")
    allowed = {
        ReleaseStage.PAPER: 0,
        ReleaseStage.SHADOW: 0,
        ReleaseStage.MICRO_LIVE: 1,
        ReleaseStage.LIMITED_LIVE: 2,
        ReleaseStage.PRODUCTION: 3,
    }
    if requested_stage not in allowed or report.maximum_stage not in allowed or allowed[requested_stage] > allowed[report.maximum_stage]:
        raise QualificationError("stage_escalation", "requested stage exceeds qualification")
    live = requested_stage in (ReleaseStage.MICRO_LIVE, ReleaseStage.LIMITED_LIVE, ReleaseStage.PRODUCTION)
    if live and not report.activation_allowed:
        raise QualificationError("live_activation_blocked", "live release requires activation_allowed")
    effective_risk = max_risk_units if live else 0.0
    if effective_risk > report.max_authorized_risk_units:
        raise QualificationError("release_risk_escalation", "release risk exceeds qualification cap")
    return ReleaseManifest(
        manifest_id=f"release:{release_version}:{generation_hash[:12]}",
        schema_version="1.0.0",
        release_version=release_version,
        source_commit=report.source_commit,
        qualification_report_hash=report.report_hash,
        environment_hash=report.environment_hash,
        generation_hash=generation_hash,
        stage=requested_stage,
        authority_order=live,
        authority_broker=live,
        max_risk_units=effective_risk,
        approved_by=approved_by,
        approved_at_ms=approved_at_ms,
        artifact_refs=artifact_refs,
        rollback_generation_hash=rollback_generation_hash,
        expires_at_ms=expires_at_ms,
    )

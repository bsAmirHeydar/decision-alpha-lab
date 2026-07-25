from __future__ import annotations

from strategy_factory_qualification_v3.contracts import ReleaseManifest
from strategy_factory_qualification_v3.enums import ReleaseStage

from .contracts import DeploymentPlan, DeploymentTarget, OperationsPolicy, RiskEnvelope
from .enums import DeploymentStage
from .errors import OperationsError

_STAGE_ORDER = {
    DeploymentStage.FROZEN: 0,
    DeploymentStage.PAPER: 1,
    DeploymentStage.SHADOW: 2,
    DeploymentStage.MICRO_LIVE: 3,
    DeploymentStage.LIMITED_LIVE: 4,
    DeploymentStage.PRODUCTION: 5,
}
_RELEASE_MAP = {
    ReleaseStage.FROZEN: DeploymentStage.FROZEN,
    ReleaseStage.PAPER: DeploymentStage.PAPER,
    ReleaseStage.SHADOW: DeploymentStage.SHADOW,
    ReleaseStage.MICRO_LIVE: DeploymentStage.MICRO_LIVE,
    ReleaseStage.LIMITED_LIVE: DeploymentStage.LIMITED_LIVE,
    ReleaseStage.PRODUCTION: DeploymentStage.PRODUCTION,
}


def compile_deployment_plan(
    release: ReleaseManifest,
    target: DeploymentTarget,
    risk_envelope: RiskEnvelope,
    policy: OperationsPolicy,
    requested_stage: DeploymentStage,
    requested_risk_units: float,
    operator_id: str,
    approver_id: str,
    approved_at_ms: int,
    starts_at_ms: int,
    expires_at_ms: int,
    limitations: tuple[str, ...] = (),
) -> DeploymentPlan:
    if release.stage not in _RELEASE_MAP:
        raise OperationsError("release_stage", "release stage is not deployable")
    maximum_stage = _RELEASE_MAP[release.stage]
    if requested_stage not in _STAGE_ORDER or _STAGE_ORDER[requested_stage] > _STAGE_ORDER[maximum_stage]:
        raise OperationsError("stage_escalation", "requested deployment stage exceeds I18 release authority")
    if target.environment_hash != release.environment_hash:
        raise OperationsError("environment_mismatch", "deployment target does not match the qualified environment")
    if approved_at_ms >= release.expires_at_ms or expires_at_ms > release.expires_at_ms:
        raise OperationsError("release_expired", "deployment plan cannot outlive its I18 release manifest")
    if approved_at_ms > starts_at_ms or starts_at_ms >= expires_at_ms:
        raise OperationsError("plan_timeline", "deployment plan timeline is invalid")
    if policy.require_distinct_operator_approver and operator_id == approver_id:
        raise OperationsError("separation_of_duties", "operator and approver must be distinct")
    live = requested_stage in (DeploymentStage.MICRO_LIVE, DeploymentStage.LIMITED_LIVE, DeploymentStage.PRODUCTION)
    effective_risk = requested_risk_units if live else 0.0
    if live and (not release.authority_order or not release.authority_broker):
        raise OperationsError("release_authority", "live deployment requires explicit order and broker authority")
    if effective_risk < 0 or effective_risk > release.max_risk_units or effective_risk > risk_envelope.max_total_risk_units:
        raise OperationsError("risk_escalation", "deployment risk exceeds release or envelope authority")
    if live and (not target.account_hashes or not target.allowed_symbols or not target.terminal_instance_ids):
        raise OperationsError("target_binding", "live deployment requires exact account, symbol and terminal bindings")
    return DeploymentPlan(
        plan_id=f"ops-plan:{release.manifest_id}:{target.target_id}:{requested_stage.value}",
        schema_version="1.0.0",
        source_commit=release.source_commit,
        release_manifest_hash=release.manifest_hash,
        qualification_report_hash=release.qualification_report_hash,
        environment_hash=release.environment_hash,
        target_hash=target.target_hash,
        generation_hash=release.generation_hash,
        rollback_generation_hash=release.rollback_generation_hash,
        stage=requested_stage,
        authority_order=live,
        authority_broker=live,
        max_risk_units=effective_risk,
        risk_envelope_hash=risk_envelope.envelope_hash,
        operator_id=operator_id,
        approver_id=approver_id,
        approved_at_ms=approved_at_ms,
        starts_at_ms=starts_at_ms,
        expires_at_ms=expires_at_ms,
        limitations=tuple(sorted(set(limitations))),
    )

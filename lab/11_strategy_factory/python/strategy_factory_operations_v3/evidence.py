from __future__ import annotations

from .contracts import EvidenceRef, GateResult, OperationsEvidenceBundle
from .enums import DeploymentStage, EvidenceState


def build_operations_evidence_bundle(
    bundle_id: str,
    source_commit: str,
    release_manifest_hash: str,
    deployment_plan_hash: str,
    policy_hash: str,
    environment_hash: str,
    generated_at_ms: int,
    gates: tuple[GateResult, ...],
    evidence_refs: tuple[EvidenceRef, ...],
    maximum_stage: DeploymentStage,
    maximum_risk_units: float,
    limitations: tuple[str, ...] = (),
) -> OperationsEvidenceBundle:
    blockers = tuple(sorted({reason for gate in gates if gate.status in (EvidenceState.FAIL, EvidenceState.PENDING) for reason in gate.reason_codes}))
    activation_allowed = not blockers and all(gate.status in (EvidenceState.PASS, EvidenceState.NOT_APPLICABLE) for gate in gates)
    if not activation_allowed:
        maximum_risk_units = 0.0
    return OperationsEvidenceBundle(
        bundle_id=bundle_id,
        schema_version="1.0.0",
        source_commit=source_commit,
        release_manifest_hash=release_manifest_hash,
        deployment_plan_hash=deployment_plan_hash,
        policy_hash=policy_hash,
        environment_hash=environment_hash,
        generated_at_ms=generated_at_ms,
        gates=tuple(sorted(gates, key=lambda item: item.gate.value)),
        evidence_refs=tuple(sorted(evidence_refs, key=lambda item: item.evidence_id)),
        activation_allowed=activation_allowed,
        maximum_stage=maximum_stage,
        maximum_risk_units=maximum_risk_units,
        blocking_reasons=blockers,
        limitations=tuple(sorted(set(limitations))),
    )

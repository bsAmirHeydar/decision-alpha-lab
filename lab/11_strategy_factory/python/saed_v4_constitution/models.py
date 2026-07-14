"""Immutable domain models for the phase-zero constitutional kernel."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any

from .canonical import stable_id
from .enums import ActorType, Authority, ClaimClass, DecisionStatus, EvidenceOperation, EvidenceRole, ReasonCode


@dataclass(frozen=True)
class Actor:
    actor_id: str
    actor_type: ActorType
    organization_unit: str
    roles: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["actor_type"] = self.actor_type.value
        d["roles"] = list(self.roles)
        return d


@dataclass(frozen=True)
class AuthorityRequest:
    program_id: str
    actor: Actor
    authority: Authority
    known_time: str
    purpose: str
    evidence_role: EvidenceRole | None = None
    payload_hashes: tuple[str, ...] = ()

    @property
    def request_id(self) -> str:
        return stable_id("authreq", self.to_dict())

    def to_dict(self) -> dict[str, Any]:
        return {
            "program_id": self.program_id,
            "actor": self.actor.to_dict(),
            "authority": self.authority.value,
            "known_time": self.known_time,
            "purpose": self.purpose,
            "evidence_role": self.evidence_role.value if self.evidence_role else None,
            "payload_hashes": list(self.payload_hashes),
        }


@dataclass(frozen=True)
class ConstitutionalDecision:
    request_id: str
    status: DecisionStatus
    reason_codes: tuple[ReasonCode, ...]
    constitution_hash: str
    policy_hash: str
    known_time: str
    details: tuple[str, ...] = ()

    @property
    def decision_id(self) -> str:
        payload = self.to_dict(include_id=False)
        return stable_id("constitution_decision", payload)

    def to_dict(self, include_id: bool = True) -> dict[str, Any]:
        result = {
            "request_id": self.request_id,
            "status": self.status.value,
            "reason_codes": [x.value for x in self.reason_codes],
            "constitution_hash": self.constitution_hash,
            "policy_hash": self.policy_hash,
            "known_time": self.known_time,
            "details": list(self.details),
        }
        if include_id:
            result["decision_id"] = self.decision_id
        return result


@dataclass(frozen=True)
class EvidenceUseRequest:
    program_id: str
    actor: Actor
    evidence_role: EvidenceRole
    operation: EvidenceOperation
    claim_class: ClaimClass
    known_time: str
    synthetic: bool = False
    positive_promotion_claim: bool = False

    @property
    def request_id(self) -> str:
        return stable_id("evidreq", self.to_dict())

    def to_dict(self) -> dict[str, Any]:
        return {
            "program_id": self.program_id,
            "actor": self.actor.to_dict(),
            "evidence_role": self.evidence_role.value,
            "operation": self.operation.value,
            "claim_class": self.claim_class.value,
            "known_time": self.known_time,
            "synthetic": self.synthetic,
            "positive_promotion_claim": self.positive_promotion_claim,
        }


@dataclass(frozen=True)
class ReviewApproval:
    reviewer_id: str
    organization_unit: str
    role: str
    known_time: str
    decision: str
    reason: str
    signature_hash: str


@dataclass(frozen=True)
class ObjectiveDefinition:
    objective_id: str
    version: str
    objective_vector: tuple[str, ...]
    hard_constraints: tuple[str, ...]
    minimum_baselines: tuple[str, ...]
    evidence_roles: tuple[EvidenceRole, ...]
    effective_from: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "objective_id": self.objective_id,
            "version": self.version,
            "objective_vector": list(self.objective_vector),
            "hard_constraints": list(self.hard_constraints),
            "minimum_baselines": list(self.minimum_baselines),
            "evidence_roles": [x.value for x in self.evidence_roles],
            "effective_from": self.effective_from,
        }


@dataclass(frozen=True)
class AmendmentProposal:
    amendment_id: str
    program_id: str
    proposer: Actor
    current_constitution_hash: str
    target_section: str
    current_value_hash: str
    proposed_value: dict[str, Any]
    rationale: str
    known_time: str
    effective_from: str
    applies_to_existing_programs: bool
    expires_at: str
    approvals: tuple[ReviewApproval, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ExposureEvent:
    program_id: str
    actor_id: str
    exposure_kind: str
    family_id: str
    known_time: str
    artifact_hash: str
    detail_hash: str

    @property
    def exposure_id(self) -> str:
        return stable_id("exposure", asdict(self))

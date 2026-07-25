"""Deterministic constitutional kernel combining authority, evidence, objectives and review gates."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .authority import AuthorityMatrix
from .canonical import content_hash
from .enums import DecisionStatus, ReasonCode
from .evidence import EvidenceFirewall
from .models import AuthorityRequest, ConstitutionalDecision, EvidenceUseRequest


@dataclass(frozen=True)
class ConstitutionPolicy:
    policy_id: str
    schema_version: str
    known_time_required: bool
    minimum_independent_approvals: int
    maximum_waiver_days: int
    complete_exposure_accounting: bool
    synthetic_positive_evidence_allowed: bool
    autonomous_promotion_allowed: bool
    autonomous_constitution_change_allowed: bool
    hard_fail_closed_states: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "schema_version": self.schema_version,
            "known_time_required": self.known_time_required,
            "minimum_independent_approvals": self.minimum_independent_approvals,
            "maximum_waiver_days": self.maximum_waiver_days,
            "complete_exposure_accounting": self.complete_exposure_accounting,
            "synthetic_positive_evidence_allowed": self.synthetic_positive_evidence_allowed,
            "autonomous_promotion_allowed": self.autonomous_promotion_allowed,
            "autonomous_constitution_change_allowed": self.autonomous_constitution_change_allowed,
            "hard_fail_closed_states": list(self.hard_fail_closed_states),
        }

    @property
    def policy_hash(self) -> str:
        return content_hash(self.to_dict())

    @classmethod
    def default(cls) -> "ConstitutionPolicy":
        return cls(
            policy_id="saed-v4-00-constitution-policy",
            schema_version="4.0.0",
            known_time_required=True,
            minimum_independent_approvals=2,
            maximum_waiver_days=90,
            complete_exposure_accounting=True,
            synthetic_positive_evidence_allowed=False,
            autonomous_promotion_allowed=False,
            autonomous_constitution_change_allowed=False,
            hard_fail_closed_states=("skip", "abstain", "manual_fallback", "reject", "quarantine"),
        )


class ConstitutionKernel:
    """Pure deterministic decision engine. It has no I/O and no external authority."""

    def __init__(
        self,
        constitution_hash: str,
        policy: ConstitutionPolicy | None = None,
        authority_matrix: AuthorityMatrix | None = None,
        evidence_firewall: EvidenceFirewall | None = None,
    ) -> None:
        if len(constitution_hash) != 64:
            raise ValueError("constitution_hash must be SHA-256 hex")
        self.constitution_hash = constitution_hash
        self.policy = policy or ConstitutionPolicy.default()
        self.authority_matrix = authority_matrix or AuthorityMatrix()
        self.evidence_firewall = evidence_firewall or EvidenceFirewall()

    def evaluate_authority(self, request: AuthorityRequest) -> ConstitutionalDecision:
        result = self.authority_matrix.evaluate(request)
        return ConstitutionalDecision(
            request_id=request.request_id,
            status=result.status,
            reason_codes=result.reasons,
            constitution_hash=self.constitution_hash,
            policy_hash=self.policy.policy_hash,
            known_time=request.known_time,
            details=result.details,
        )

    def evaluate_evidence(self, request: EvidenceUseRequest) -> ConstitutionalDecision:
        result = self.evidence_firewall.evaluate(request)
        return ConstitutionalDecision(
            request_id=request.request_id,
            status=result.status,
            reason_codes=result.reasons,
            constitution_hash=self.constitution_hash,
            policy_hash=self.policy.policy_hash,
            known_time=request.known_time,
            details=result.details,
        )

    def assert_constitution_invariants(self) -> tuple[ReasonCode, ...]:
        failures: list[ReasonCode] = []
        if self.policy.synthetic_positive_evidence_allowed:
            failures.append(ReasonCode.SYNTHETIC_POSITIVE_PROMOTION)
        if self.policy.autonomous_promotion_allowed:
            failures.append(ReasonCode.AUTHORITY_DENIED)
        if self.policy.autonomous_constitution_change_allowed:
            failures.append(ReasonCode.AUTHORITY_DENIED)
        if self.policy.minimum_independent_approvals < 2:
            failures.append(ReasonCode.MISSING_SECOND_APPROVAL)
        return tuple(failures)

    def health(self) -> dict[str, Any]:
        failures = self.assert_constitution_invariants()
        return {
            "status": DecisionStatus.ALLOW.value if not failures else DecisionStatus.REJECT.value,
            "constitution_hash": self.constitution_hash,
            "policy_hash": self.policy.policy_hash,
            "failures": [x.value for x in failures],
        }

"""Conformance-vector runner for constitutional golden and negative cases."""
from __future__ import annotations

from typing import Any

from .enums import ActorType, Authority, ClaimClass, EvidenceOperation, EvidenceRole
from .models import Actor, AuthorityRequest, EvidenceUseRequest
from .policy import ConstitutionKernel


def run_vector(kernel: ConstitutionKernel, vector: dict[str, Any]) -> dict[str, Any]:
    actor_data = vector["actor"]
    actor = Actor(
        actor_id=actor_data["actor_id"],
        actor_type=ActorType(actor_data["actor_type"]),
        organization_unit=actor_data["organization_unit"],
        roles=tuple(actor_data.get("roles", [])),
    )
    if vector["request_type"] == "authority":
        request = AuthorityRequest(
            program_id=vector["program_id"],
            actor=actor,
            authority=Authority(vector["authority"]),
            known_time=vector["known_time"],
            purpose=vector["purpose"],
            evidence_role=EvidenceRole(vector["evidence_role"]) if vector.get("evidence_role") else None,
            payload_hashes=tuple(vector.get("payload_hashes", [])),
        )
        decision = kernel.evaluate_authority(request)
    elif vector["request_type"] == "evidence":
        request = EvidenceUseRequest(
            program_id=vector["program_id"],
            actor=actor,
            evidence_role=EvidenceRole(vector["evidence_role"]),
            operation=EvidenceOperation(vector["operation"]),
            claim_class=ClaimClass(vector["claim_class"]),
            known_time=vector["known_time"],
            synthetic=bool(vector.get("synthetic", False)),
            positive_promotion_claim=bool(vector.get("positive_promotion_claim", False)),
        )
        decision = kernel.evaluate_evidence(request)
    else:
        raise ValueError(f"unknown request_type: {vector['request_type']}")
    result = decision.to_dict()
    result["matches_expected"] = (
        result["status"] == vector["expected_status"]
        and set(result["reason_codes"]) == set(vector["expected_reason_codes"])
    )
    return result

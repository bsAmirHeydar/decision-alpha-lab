from __future__ import annotations

from .canonical import content_hash, seal, stable_id
from .contracts import UpstreamIntakeContract
from .errors import UpstreamVerificationError

REQUIRED_HANDOFF_WORK = {
    "continual_calibration_research",
    "meta_learning_dataset_design",
    "transfer_shift_mapping",
    "drift_segment_taxonomy",
    "safe_recalibration_experiments",
}


def verify(contract: UpstreamIntakeContract, documents: dict) -> dict:
    if set(documents) != {"handoff", "certificate"}:
        raise UpstreamVerificationError("upstream documents must contain handoff and certificate only")
    handoff = documents["handoff"]
    certificate = documents["certificate"]
    if handoff.get("phase") != "SAED_V4_24" or handoff.get("next_phase") != "SAED_V4_25":
        raise UpstreamVerificationError("wrong V4-24 handoff phase")
    if certificate.get("phase") != "SAED_V4_24":
        raise UpstreamVerificationError("wrong V4-24 certificate phase")
    if handoff.get("handoff_hash") != contract.handoff_hash:
        raise UpstreamVerificationError("handoff hash does not match frozen intake")
    if certificate.get("certificate_hash") != contract.certificate_hash:
        raise UpstreamVerificationError("certificate hash does not match frozen intake")
    if handoff.get("certificate_hash") != certificate.get("certificate_hash"):
        raise UpstreamVerificationError("handoff and certificate are not linked")
    if handoff.get("research_policy_id") != contract.research_policy_id:
        raise UpstreamVerificationError("research policy identity mismatch")
    if set(handoff.get("allowed_next_work", [])) != REQUIRED_HANDOFF_WORK:
        raise UpstreamVerificationError("V4-24 handoff scope mismatch")
    if not handoff.get("research_only") or any(handoff.get("authority", {}).values()):
        raise UpstreamVerificationError("upstream authority boundary is unsafe")
    if not certificate.get("accepted_for_conformal_ood_selective_research"):
        raise UpstreamVerificationError("V4-24 certificate was not accepted")
    if not certificate.get("selection_is_research_only"):
        raise UpstreamVerificationError("V4-24 selection boundary missing")
    forbidden_claims = (
        certificate.get("promotion_authority"),
        certificate.get("runtime_executable"),
        certificate.get("risk_allocation_authority"),
        certificate.get("execution_authority"),
        certificate.get("production_authority"),
        certificate.get("real_alpha_claim"),
        certificate.get("prospective_success_claim"),
    )
    if any(forbidden_claims):
        raise UpstreamVerificationError("upstream certificate contains forbidden authority or claims")
    payload = {
        "phase": "SAED_V4_25",
        "upstream_phase": "SAED_V4_24",
        "handoff_hash": contract.handoff_hash,
        "certificate_hash": contract.certificate_hash,
        "research_policy_id": contract.research_policy_id,
        "documents_hash": content_hash(documents),
        "scope_verified": True,
        "immutable": True,
        "research_only": True,
        "authority_denied": True,
    }
    payload["receipt_id"] = stable_id("upstream_receipt", payload)
    return seal(payload, "receipt_hash")

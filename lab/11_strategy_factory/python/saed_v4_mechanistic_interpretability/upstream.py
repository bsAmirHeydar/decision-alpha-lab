from __future__ import annotations
from typing import Any
from .canonical import content_hash, stable_id
from .contracts import UpstreamIntakeContract
from .errors import UpstreamVerificationError

def verify(contract:UpstreamIntakeContract, documents:dict[str,Any])->dict[str,Any]:
    if set(documents)!={"certificate","handoff","frozen_artifacts"}: raise UpstreamVerificationError("upstream document set mismatch")
    cert,handoff,frozen=documents["certificate"],documents["handoff"],documents["frozen_artifacts"]
    if cert.get("phase")!="SAED_V4_25" or handoff.get("phase")!="SAED_V4_25" or handoff.get("next_phase")!="SAED_V4_26": raise UpstreamVerificationError("phase mismatch")
    if cert.get("certificate_hash")!=contract.certificate_hash or handoff.get("handoff_hash")!=contract.handoff_hash: raise UpstreamVerificationError("declared hash mismatch")
    if not cert.get("accepted_for_continual_meta_transfer_research") or not handoff.get("research_only"): raise UpstreamVerificationError("upstream research acceptance missing")
    if any(handoff.get("authority",{}).values()): raise UpstreamVerificationError("upstream authority nonzero")
    required={"GOLDEN_ADAPTATIONS.JSON","GOLDEN_CONTINUAL_CALIBRATION_STATES.JSON","GOLDEN_DRIFT_REPORT.JSON","GOLDEN_META_FEATURES.JSON","GOLDEN_TRANSFER_MAP.JSON","GOLDEN_TRANSFER_REPORT.JSON","GOLDEN_REPLAY_RECEIPT.JSON"}
    if set(frozen)!=required: raise UpstreamVerificationError("frozen artifact set mismatch")
    payload={"phase":"SAED_V4_26","upstream_phase":"SAED_V4_25","certificate_hash":contract.certificate_hash,"handoff_hash":contract.handoff_hash,"frozen_artifact_hashes":{k:content_hash(v) for k,v in sorted(frozen.items())},"immutable":True,"hash_verified":True,"research_only":True}
    payload["upstream_receipt_id"]=stable_id("v4_25_receipt",payload)
    payload["upstream_receipt_hash"]=content_hash(payload)
    return payload

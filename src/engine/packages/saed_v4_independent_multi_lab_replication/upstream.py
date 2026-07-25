from __future__ import annotations
from .canonical import content_hash,stable_id
from .contracts import require_exact
from .errors import IntegrityError

CERTIFICATE_HASH="e9b8d03f357ce46143be9b6a6ef55729b0b1e755da6164345e334bfb54078931"
HANDOFF_HASH="cb6f30891554c37dcc1acf0a316af7230529bbbd8658bddef784e1850d38594e"

def verify_upstream(documents:dict)->dict:
    require_exact(documents,["certificate","handoff"],name="upstream_documents")
    certificate=documents["certificate"]; handoff=documents["handoff"]
    if certificate.get("certificate_hash")!=CERTIFICATE_HASH or content_hash({k:v for k,v in certificate.items() if k!="certificate_hash"})!=CERTIFICATE_HASH: raise IntegrityError("V4-29 certificate hash mismatch")
    if handoff.get("handoff_hash")!=HANDOFF_HASH or content_hash({k:v for k,v in handoff.items() if k!="handoff_hash"})!=HANDOFF_HASH: raise IntegrityError("V4-29 handoff hash mismatch")
    if certificate.get("phase")!="SAED_V4_29" or certificate.get("version")!="1.0.0" or certificate.get("claim_class")!="hidden_evaluation_air_gap_closed_reference_implementation": raise IntegrityError("invalid V4-29 certificate")
    if handoff.get("phase")!="SAED_V4_29" or handoff.get("next_phase")!="SAED_V4_30" or not handoff.get("research_only"): raise IntegrityError("invalid V4-29 handoff")
    if certificate.get("certificate_id")!=handoff.get("certificate_id"): raise IntegrityError("certificate identity mismatch")
    if certificate.get("certificate_hash")!=handoff.get("certificate_hash"): raise IntegrityError("certificate binding mismatch")
    required={"independent_replication_protocol","multi_lab_package_identity","replication_lab_registration","blinded_artifact_exchange","cross_lab_hash_reconciliation","replication_disagreement_report","external_custody_evidence_attachment"}
    if not required.issubset(set(handoff.get("allowed_next_work",[]))): raise IntegrityError("handoff scope incomplete")
    receipt={"phase":"SAED_V4_30","upstream_phase":"SAED_V4_29","certificate_id":certificate["certificate_id"],"certificate_hash":CERTIFICATE_HASH,"handoff_id":handoff["handoff_id"],"handoff_hash":HANDOFF_HASH,"verified":True,"research_only":True}
    receipt["receipt_id"]=stable_id("v430_upstream",receipt); receipt["receipt_hash"]=content_hash(receipt)
    return receipt

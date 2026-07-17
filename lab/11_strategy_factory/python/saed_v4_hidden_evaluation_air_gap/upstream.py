from __future__ import annotations
from .canonical import content_hash,stable_id
from .errors import IntegrityError
EXPECTED_CERTIFICATE_HASH="eb70719041cb2ef6968adbc1c5343ed84476dbd3a12e58250316db4dbdd3b153"
EXPECTED_HANDOFF_HASH="bfe958a8decdec375994d091cec4b4993aba0d213a57ad78297e34d70a534b66"

def verify(intake,docs):
    if set(docs)!={"certificate","handoff"}: raise IntegrityError("upstream documents must be exact")
    cert=docs["certificate"]; handoff=docs["handoff"]
    if cert.get("certificate_hash")!=EXPECTED_CERTIFICATE_HASH or handoff.get("handoff_hash")!=EXPECTED_HANDOFF_HASH: raise IntegrityError("unexpected canonical V4-28 hashes")
    if intake.certificate_hash!=cert["certificate_hash"] or intake.handoff_hash!=handoff["handoff_hash"] or intake.certificate_id!=cert["certificate_id"] or intake.handoff_id!=handoff["handoff_id"]: raise IntegrityError("upstream intake binding mismatch")
    if not cert.get("accepted_for_online_fdr_research_reference") or not cert.get("research_only") or cert.get("hidden_evaluation_air_gap_claim") is not False: raise IntegrityError("upstream certificate claim mismatch")
    if handoff.get("next_phase")!="SAED_V4_29" or not handoff.get("entry_gates",{}).get("protected_evidence_access_zero") or any(handoff.get("authority",{}).values()): raise IntegrityError("unsafe V4-28 handoff")
    body={"phase":"SAED_V4_29","upstream_phase":"SAED_V4_28","certificate_id":cert["certificate_id"],"certificate_hash":cert["certificate_hash"],"handoff_id":handoff["handoff_id"],"handoff_hash":handoff["handoff_hash"],"verified":True,"immutable":True,"research_only":True}
    body["receipt_id"]=stable_id("v429_upstream",body); body["receipt_hash"]=content_hash(body); return body

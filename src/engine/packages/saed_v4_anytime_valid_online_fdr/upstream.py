from __future__ import annotations
from .canonical import content_hash, stable_id
from .errors import IntegrityError

def verify(intake,documents):
    required={"certificate","handoff","multiplicity_universe","complete_trial_ledger","complete_exposure_ledger","integrity_report"}
    if set(documents)!=required: raise IntegrityError("upstream document set mismatch")
    cert=documents["certificate"]; handoff=documents["handoff"]; universe=documents["multiplicity_universe"]
    if cert.get("phase")!="SAED_V4_27" or cert.get("certificate_hash")!=intake.certificate_hash: raise IntegrityError("V4-27 certificate mismatch")
    if handoff.get("next_phase")!="SAED_V4_28" or handoff.get("handoff_hash")!=intake.handoff_hash: raise IntegrityError("V4-27 handoff mismatch")
    if universe.get("multiplicity_universe_hash")!=intake.multiplicity_universe_hash: raise IntegrityError("multiplicity universe mismatch")
    if not cert.get("accepted_for_complete_ledger_research") or not handoff.get("research_only"): raise IntegrityError("upstream gate not accepted")
    if not documents["complete_trial_ledger"].get("complete") or not documents["complete_exposure_ledger"].get("complete") or not documents["integrity_report"].get("passed"): raise IntegrityError("upstream completeness failure")
    payload={"phase":"SAED_V4_28","required_phase":"SAED_V4_27","certificate_id":cert["certificate_id"],"certificate_hash":cert["certificate_hash"],"handoff_id":handoff["handoff_id"],"handoff_hash":handoff["handoff_hash"],"multiplicity_universe_id":universe["multiplicity_universe_id"],"multiplicity_universe_hash":universe["multiplicity_universe_hash"],"family_count":universe["family_count"],"trial_count":universe["trial_count"],"exposure_count":universe["exposure_count"],"immutable":True,"hash_verified":True,"research_only":True}
    payload["receipt_id"]=stable_id("v428_upstream_receipt",payload); payload["receipt_hash"]=content_hash(payload); return payload

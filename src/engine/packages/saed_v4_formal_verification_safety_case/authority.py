from __future__ import annotations
from .canonical import content_hash,stable_id
from .errors import VerificationError

def boundary()->dict:
    authority={"research_decision":False,"promotion":False,"runtime":False,"risk_allocation":False,"execution":False,"production":False,"online_learning":False,"live_trading":False,"specification_override":False,"counterexample_suppression":False,"residual_risk_waiver":False,"external_proof_claim":False}
    body={"phase":"SAED_V4_31","authority":authority,"safe_action":"quarantine","ucee_authority_preserved":True,"formal_verification_is_evidence_not_permission":True,"research_only":True}; body["boundary_id"]=stable_id("v431_authority",body); body["boundary_hash"]=content_hash(body); return body

def assert_zero(value:dict)->None:
    if any(value["authority"].values()): raise VerificationError("V4-31 authority must remain zero")

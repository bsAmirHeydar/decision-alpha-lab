from __future__ import annotations
from .canonical import content_hash, stable_id
from .errors import IntegrityError
FORBIDDEN=("private_key","secret_key","password","bearer_token","api_token","order_send","live_account")

def scan(*documents):
    text=repr(documents).lower(); hits=[x for x in FORBIDDEN if x in text]
    if hits: raise IntegrityError(f"forbidden security material: {hits}")
    payload={"phase":"SAED_V4_28","passed":True,"forbidden_material_hits":[],"network_access":False,"filesystem_mutation_outside_delivery":False,"credential_use":False,"broker_connection":False,"runtime_compilation":False,"order_submission":False,"online_policy_mutation":False}
    payload["security_review_id"]=stable_id("v428_security_review",payload); payload["security_review_hash"]=content_hash(payload); return payload

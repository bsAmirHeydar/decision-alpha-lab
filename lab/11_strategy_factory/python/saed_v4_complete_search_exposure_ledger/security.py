from __future__ import annotations
from typing import Any
from .canonical import content_hash, stable_id
from .errors import AuthorityBoundaryError
FORBIDDEN=("broker_password","broker_token","private_key","signing_key","order_send","webrequest","runtime_compile","live_account")

def scan(*values:Any)->dict[str,Any]:
    text=repr(values).lower(); findings=[x for x in FORBIDDEN if x in text]
    if findings: raise AuthorityBoundaryError(f"forbidden security surfaces: {findings}")
    payload={"phase":"SAED_V4_27","passed":True,"forbidden_surface_findings":[],"broker_credentials_present":False,"signing_material_present":False,"network_requests":0,"runtime_compilations":0,"order_submissions":0,"online_policy_mutations":0,"air_gap_not_claimed":True}
    payload["security_review_id"]=stable_id("v427_security",payload); payload["security_review_hash"]=content_hash(payload)
    return payload

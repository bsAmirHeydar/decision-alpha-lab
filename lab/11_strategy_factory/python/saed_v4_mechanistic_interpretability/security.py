from __future__ import annotations
from typing import Any
from .canonical import content_hash, stable_id
from .errors import SecurityBoundaryError
FORBIDDEN=("password","secret_key","private_key","broker_token","ordersend","webrequest","socketcreate")
def scan(config:dict[str,Any], records:list[dict[str,Any]])->dict[str,Any]:
    blob=(str(config)+str(records)).lower()
    findings=[token for token in FORBIDDEN if token in blob]
    if findings: raise SecurityBoundaryError(f"forbidden security surface: {findings}")
    report={"phase":"SAED_V4_26","passed":True,"network_access":False,"broker_credentials_present":False,"signing_material_present":False,"order_surface_present":False,"findings":[]}
    report["security_review_id"]=stable_id("security_review",report); report["security_review_hash"]=content_hash(report)
    return report

from __future__ import annotations
from .canonical import content_hash,stable_id
from .errors import AuthorityError

AUTHORITY_KEYS=["research_decision","promotion","runtime","risk_allocation","execution","production","online_learning","live_trading","raw_hidden_data_export","adaptive_replication","rerun_authority"]

def boundary()->dict:
    authority={k:False for k in AUTHORITY_KEYS}
    body={"phase":"SAED_V4_30","authority":authority,"research_only":True,"synthetic_fixture_only":True,"independent_external_reproduction":False,"ucee_authority_preserved":True,"safe_action":"quarantine"}
    body["boundary_id"]=stable_id("v430_authority",body); body["boundary_hash"]=content_hash(body); return body

def assert_zero(value:dict)->None:
    if any(value["authority"].values()): raise AuthorityError("V4-30 may not acquire authority")

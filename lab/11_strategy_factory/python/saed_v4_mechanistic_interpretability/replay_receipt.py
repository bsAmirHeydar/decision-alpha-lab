from __future__ import annotations
from typing import Any
from .canonical import content_hash, stable_id
def build(config:dict[str,Any], records:list[dict[str,Any]], outputs:dict[str,Any])->dict[str,Any]:
    payload={"phase":"SAED_V4_26","config_hash":content_hash(config),"records_hash":content_hash(records),"output_hashes":{k:content_hash(v) for k,v in sorted(outputs.items())},"deterministic":True,"network_access":False,"future_suffix_queries":0,"protected_evidence_queries":0,"hidden_evaluation_queries":0,"runtime_compilations":0,"order_submissions":0,"online_policy_mutations":0}
    payload["replay_receipt_id"]=stable_id("mechanistic_replay",payload); payload["replay_receipt_hash"]=content_hash(payload)
    return payload

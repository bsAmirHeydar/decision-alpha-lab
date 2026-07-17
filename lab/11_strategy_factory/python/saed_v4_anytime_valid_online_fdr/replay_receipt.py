from __future__ import annotations
from .canonical import content_hash, stable_id

def build(config,hypotheses,outputs):
    payload={"phase":"SAED_V4_28","config_hash":content_hash(config),"hypothesis_stream_hash":content_hash(hypotheses),"output_hashes":{k:content_hash(v) for k,v in outputs.items()},"deterministic":True,"network_access":False,"future_suffix_invariant":True,"random_seed_required":False,"replay_command":"python tools/strategy_factory/saed_v4_28/reproduce_saed_v4_28_golden.py"}
    payload["replay_id"]=stable_id("v428_replay",payload); payload["replay_hash"]=content_hash(payload); return payload

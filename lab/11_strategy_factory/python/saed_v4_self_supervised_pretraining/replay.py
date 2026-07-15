from __future__ import annotations
from .canonical import content_hash, stable_id

def build_replay_receipt(expected:dict,actual:dict)->dict:
    fields=sorted(set(expected)&set(actual))
    comparisons={k:expected[k]==actual[k] for k in fields if k.endswith('_hash') or k.endswith('_id') or k in {'total_pairs','deterministic','status'}}
    payload={"phase":"SAED_V4_11","comparisons":comparisons,"comparison_count":len(comparisons),"passed":all(comparisons.values()),"expected_content_hash":content_hash(expected),"actual_content_hash":content_hash(actual)}
    payload['replay_id']=stable_id('v411replay',payload);payload['replay_hash']=content_hash(payload);return payload

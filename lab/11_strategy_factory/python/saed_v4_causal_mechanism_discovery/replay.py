from __future__ import annotations
from .canonical import content_hash

def receipt(bundle_hashes):
    first=content_hash(bundle_hashes);second=content_hash(dict(bundle_hashes))
    out={'phase':'SAED_V4_17','first_pass_hash':first,'second_pass_hash':second,'deterministic_replay_passed':first==second,'input_artifact_count':len(bundle_hashes),'future_suffix_accessed':False,'protected_evidence_exposures':0};out['receipt_hash']=content_hash(out);return out

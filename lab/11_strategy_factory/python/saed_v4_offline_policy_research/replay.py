from __future__ import annotations
from .canonical import content_hash,stable_id

def receipt(config_hash,input_hashes,output_hashes):
    core={'phase':'SAED_V4_23','config_hash':config_hash,'input_hashes':dict(sorted(input_hashes.items())),'output_hashes':dict(sorted(output_hashes.items())),'deterministic':True,'future_suffix_sensitive':False,'protected_evidence_queries':0,'hidden_evaluation_queries':0}
    core['replay_id']=stable_id('replay',core);core['replay_hash']=content_hash(core);return core

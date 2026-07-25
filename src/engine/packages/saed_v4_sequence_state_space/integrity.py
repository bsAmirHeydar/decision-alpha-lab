from __future__ import annotations
from .canonical import content_hash,merkle_root,stable_id

def build_integrity_receipt(named):
    hashes=[];entries=[]
    for name,doc in sorted(named.items()):
        h=content_hash(doc);hashes.append(h);entries.append({'name':name,'content_hash':h})
    material={'phase':'SAED_V4_12','entries':entries,'merkle_root':merkle_root(hashes),'artifact_count':len(entries),'canonicalization':'sorted_compact_json_v1'}
    return {**material,'receipt_id':stable_id('seqintegrity',material),'receipt_hash':content_hash(material)}

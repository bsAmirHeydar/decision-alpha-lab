from __future__ import annotations
from .canonical import content_hash

def receipt(artifacts):
    rows=[{'artifact_id':k,'artifact_hash':content_hash(v)} for k,v in sorted(artifacts.items())]
    return {'phase':'SAED_V4_19','artifacts':rows,'artifact_count':len(rows),'receipt_hash':content_hash(rows),'immutable':True}

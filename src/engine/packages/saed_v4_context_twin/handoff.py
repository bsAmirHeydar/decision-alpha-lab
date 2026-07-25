from __future__ import annotations
from .canonical import content_hash,stable_id

def build_v4_03_handoff(manifest,snapshot,receipt,limitations):
    payload={'phase':'SAED_V4_02','next_phase':'SAED_V4_03','twin_id':manifest.twin_id,'twin_version':manifest.exact_version,'manifest_hash':manifest.semantic_hash,'snapshot_hash':snapshot.snapshot_hash,'integrity_receipt_id':receipt.receipt_id,'known_as_of':snapshot.known_as_of,'limitations':sorted(set(limitations)),'authority':manifest.authority.to_dict(),'golden_gate':'same manifest plus same event stream yields same state snapshot'}
    return {**payload,'handoff_id':stable_id('handoff',payload),'handoff_hash':content_hash(payload)}

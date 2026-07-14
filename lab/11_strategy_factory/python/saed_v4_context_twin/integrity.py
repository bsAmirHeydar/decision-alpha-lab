from __future__ import annotations
from .models import TwinIntegrityReceipt
from .canonical import merkle_root

def build_receipt(manifest,snapshot):
    root=merkle_root([manifest.semantic_hash,snapshot.snapshot_hash,*snapshot.observation_ids,*snapshot.contradiction_ids,*snapshot.evidence_debt_ids,*snapshot.transition_event_ids])
    return TwinIntegrityReceipt(manifest.twin_id,manifest.semantic_hash,snapshot.snapshot_hash,root,'verified',{'component_count':2+len(snapshot.observation_ids)+len(snapshot.contradiction_ids)+len(snapshot.evidence_debt_ids)+len(snapshot.transition_event_ids)})
def verify_receipt(receipt,manifest,snapshot):
    return receipt==build_receipt(manifest,snapshot)

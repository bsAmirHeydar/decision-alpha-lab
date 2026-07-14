from .models import EventIntegrityReceipt
from .canonical import merkle_root
from .errors import IntegrityError

def build_integrity_receipt(twin_id,journal_root,manifests,watermarks,projection=None,details=None):
    leaves=[journal_root]+[m.semantic_hash for m in manifests]+[w.watermark_id for w in watermarks]
    if projection:leaves.append(projection.state_hash)
    return EventIntegrityReceipt(twin_id,journal_root,projection.state_hash if projection else None,tuple(sorted(m.semantic_hash for m in manifests)),tuple(sorted(w.watermark_id for w in watermarks)),merkle_root(leaves),'pass',details or {})
def verify_integrity_receipt(receipt,manifests,watermarks,projection=None):
    candidate=build_integrity_receipt(receipt.twin_id,receipt.journal_root,manifests,watermarks,projection,receipt.details)
    if candidate.component_root!=receipt.component_root:raise IntegrityError('event integrity receipt mismatch')
    return True

from __future__ import annotations
from .canonical import canonical_sha256,stable_id
from .contracts import RevisionInvalidation

def compute_invalidation(revision,pair_windows,references):
    affected_windows=tuple(sorted(w.pair_window_id for w in pair_windows if w.descriptor.start_utc_ms<revision.affected_end_utc_ms and revision.affected_start_utc_ms<w.descriptor.end_utc_ms))
    affected_refs=tuple(sorted(r.reference_id for r in references if r.source_pair_window_id in set(affected_windows)))
    prefix=[w.semantic_hash for w in pair_windows if w.descriptor.end_utc_ms<=revision.affected_start_utc_ms]
    material={'revision':revision.revision_id,'windows':affected_windows,'refs':affected_refs,'prefix':prefix}
    return RevisionInvalidation(stable_id('FPINVALIDATE',material,32),revision.revision_id,affected_windows,affected_refs,canonical_sha256(prefix),'FP_RRC_REVISION_INVALIDATION_COMPUTED',canonical_sha256(material))

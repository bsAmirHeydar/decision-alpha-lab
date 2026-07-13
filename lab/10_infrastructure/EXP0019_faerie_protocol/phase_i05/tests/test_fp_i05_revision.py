from dataclasses import replace
from fp_i05_reference.golden import golden_completed_n_window
from fp_i05_reference.revision import compute_invalidation

def test_revision_invalidates_only_overlapping_windows_and_references():
 cfg,result,desc,agg,refs=golden_completed_n_window();rev=replace(result.revision,affected_start_utc_ms=desc.start_utc_ms,affected_end_utc_ms=desc.start_utc_ms+60000)
 inv=compute_invalidation(rev,(agg,),refs.references)
 assert inv.affected_pair_window_ids==(agg.pair_window_id,) and len(inv.affected_reference_ids)==4

def test_revision_after_window_does_not_invalidate_window():
 cfg,result,desc,agg,refs=golden_completed_n_window();rev=replace(result.revision,affected_start_utc_ms=desc.end_utc_ms+60000,affected_end_utc_ms=desc.end_utc_ms+120000)
 inv=compute_invalidation(rev,(agg,),refs.references)
 assert inv.affected_pair_window_ids==() and inv.affected_reference_ids==()

def test_invalidation_is_deterministic():
 cfg,result,desc,agg,refs=golden_completed_n_window();a=compute_invalidation(result.revision,(agg,),refs.references);b=compute_invalidation(result.revision,(agg,),refs.references)
 assert a.evidence_hash==b.evidence_hash

from fp_i07_confirmation import *
from fp_i07_confirmation.golden import golden_case

def test_overlap_invalidates_pending():
    *_,p,o,r,events=golden_case();i=assess_revision(p,'REV-2',p.candidate.first_hunt_minute_utc_ms,p.projection.target_close_utc_ms);assert i.disposition is RevisionDisposition.PENDING_INVALIDATED
def test_nonoverlap_does_not_invalidate_pending():
    *_,p,o,r,events=golden_case();i=assess_revision(p,'REV-2',p.projection.deadline_utc_ms,p.projection.deadline_utc_ms+60_000);assert i.disposition is RevisionDisposition.UNAFFECTED
def test_confirmed_signal_preserved():
    *_,p,o,r,events=golden_case();i=assess_revision(r,'REV-2',p.candidate.first_hunt_minute_utc_ms,p.projection.target_close_utc_ms);assert i.disposition is RevisionDisposition.CONFIRMED_PRESERVED
def test_revision_impact_deterministic():
    *_,p,o,r,events=golden_case();assert assess_revision(r,'REV-2',0,60_000)==assess_revision(r,'REV-2',0,60_000)

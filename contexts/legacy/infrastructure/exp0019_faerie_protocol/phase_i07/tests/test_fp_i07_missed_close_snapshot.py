from fp_i07_confirmation import *
from fp_i07_confirmation.golden import golden_case

def test_missed_close_requires_replay():
    c,cfg,b,pj,p,o,r,events=golden_case();mr,ev=mark_missed_close(p,b.close_utc_ms+60_000,cfg);assert mr.outcome is ConfirmationOutcome.MISSED_CLOSE_REPLAY_REQUIRED
def test_missed_close_not_marked_early():
    import pytest
    c,cfg,b,pj,p,o,r,events=golden_case()
    with pytest.raises(Exception):mark_missed_close(p,b.close_utc_ms,cfg)
def test_snapshot_contains_immutable_signal():
    c,cfg,b,pj,p,o,r,events=golden_case();s=build_snapshot(cfg,(p,),(r,),events,b.close_utc_ms,'REV-1');assert len(s.signals)==1 and not s.pending
def test_snapshot_blocked_on_missed_close():
    c,cfg,b,pj,p,o,r,events=golden_case();mr,ev=mark_missed_close(p,b.close_utc_ms+60_000,cfg);s=build_snapshot(cfg,(p,),(mr,),events+(ev,),b.close_utc_ms+60_000,'REV-1');assert s.health is EngineHealth.BLOCKED

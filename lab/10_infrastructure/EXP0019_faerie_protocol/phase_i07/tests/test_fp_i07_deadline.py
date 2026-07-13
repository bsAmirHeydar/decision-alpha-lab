from fp_i07_confirmation import *
from fp_i07_confirmation.golden import candidate,config,host_bar
from fp_i07_confirmation.observation import observe_close

def setup(deadline_offset):
    seed=candidate();cfg=config();probe=host_bar(seed)
    deadline=probe.close_utc_ms if deadline_offset==300_000 else seed.first_hunt_minute_utc_ms+deadline_offset
    c=candidate(first=seed.first_hunt_minute_utc_ms,deadline=deadline);b=host_bar(c);p=project_candidate(c,(b,),cfg);pending,_=admit_candidate(c,p,'REV-1',c.first_hunt_minute_utc_ms);o=observe_close(c,b,ClosePairState.HUNTER_ONLY,b.close_utc_ms,'REV-1');return c,cfg,b,pending,o
def test_close_equal_deadline_expires():
    c,cfg,b,p,o=setup(300_000);assert b.close_utc_ms==c.check_end_utc_ms;assert finalize(p,b,o,cfg)[0].outcome is ConfirmationOutcome.CONFIRMATION_DEADLINE_MISSED
def test_close_after_deadline_expires():
    c,cfg,b,p,o=setup(60_000);assert finalize(p,b,o,cfg)[0].final_state is ConfirmationState.EXPIRED_DEADLINE
def test_expire_without_close_at_deadline():
    c,cfg,b,p,o=setup(300_000);assert expire_without_close(p,c.check_end_utc_ms,cfg)[0].outcome is ConfirmationOutcome.CONFIRMATION_DEADLINE_MISSED
def test_cannot_expire_before_deadline():
    import pytest
    c,cfg,b,p,o=setup(300_000)
    with pytest.raises(Exception):expire_without_close(p,c.check_end_utc_ms-60_000,cfg)
def test_candidate_never_migrates_session():
    c,cfg,b,p,o=setup(300_000);r,_=finalize(p,b,o,cfg);assert r.projection_id==p.projection.projection_id

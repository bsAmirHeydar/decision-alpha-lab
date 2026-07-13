from fp_i07_confirmation import *
from fp_i07_confirmation.golden import candidate,config,host_bar
from fp_i07_confirmation.observation import observe_close

def setup(coverage=True,available=None,closed=True):
    c=candidate();cfg=config();b=host_bar(c,coverage=coverage,closed=closed);p=project_candidate(c,(b,),cfg);pending,_=admit_candidate(c,p,'REV-1',c.first_hunt_minute_utc_ms);o=observe_close(c,b,ClosePairState.HUNTER_ONLY,available if available is not None else b.close_utc_ms,'REV-1');return cfg,b,pending,o
def test_incomplete_coverage_blocks_confirmation():
    cfg,b,p,o=setup(False);assert finalize(p,b,o,cfg)[0].outcome is ConfirmationOutcome.UNAVAILABLE_AT_CLOSE
def test_source_not_available_through_close_blocks():
    cfg,b,p,o=setup(True);object.__setattr__(o,'source_available_through_utc_ms',b.close_utc_ms-60_000);assert finalize(p,b,o,cfg)[0].outcome is ConfirmationOutcome.UNAVAILABLE_AT_CLOSE
def test_open_host_bar_cannot_finalize():
    import pytest
    cfg,b,p,o=setup(closed=False)
    with pytest.raises(Exception):finalize(p,b,o,cfg)
def test_target_bar_mismatch_rejected():
    import pytest
    cfg,b,p,o=setup();object.__setattr__(b,'host_bar_id','OTHER')
    with pytest.raises(Exception):finalize(p,b,o,cfg)
def test_bar_availability_not_before_close_contract():
    import pytest
    c=candidate();b=host_bar(c);object.__setattr__(b,'availability_utc_ms',b.close_utc_ms-1)
    with pytest.raises(Exception):b.__post_init__()

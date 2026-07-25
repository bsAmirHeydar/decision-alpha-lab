import pytest
from fp_i07_confirmation import *
from fp_i07_confirmation.golden import golden_case

def test_checkpoint_roundtrip_validates():
    c,cfg,b,pj,p,o,r,events=golden_case();cp=build_checkpoint(cfg,(p,),(r,),b.close_utc_ms,'REV-1');assert validate_checkpoint(cp,cfg)
def test_checkpoint_config_mismatch_rejected():
    c,cfg,b,pj,p,o,r,events=golden_case();cp=build_checkpoint(cfg,(p,),(),b.close_utc_ms,'REV-1')
    from fp_i07_confirmation.golden import config
    with pytest.raises(Exception):validate_checkpoint(cp,config(HostTimeframe.M15))
def test_checkpoint_corruption_rejected():
    c,cfg,b,pj,p,o,r,events=golden_case();cp=build_checkpoint(cfg,(p,),(),b.close_utc_ms,'REV-1');object.__setattr__(cp,'payload_hash','0'*64)
    with pytest.raises(Exception):validate_checkpoint(cp,cfg)
def test_restart_preserves_signal_identity():
    c,cfg,b,pj,p,o,r,events=golden_case();cp=build_checkpoint(cfg,(),(r,),b.close_utc_ms,'REV-1');validate_checkpoint(cp,cfg);assert cp.results[0].confirmed_signal.signal_id==r.confirmed_signal.signal_id

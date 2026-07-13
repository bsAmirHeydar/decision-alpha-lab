import pytest
from fp_i07_confirmation import *
from fp_i07_confirmation.golden import candidate,config,host_bar

def test_period_current_rejected():
    with pytest.raises(Exception): resolve_timeframe('PERIOD_CURRENT')
def test_supported_timeframe_resolves(): assert resolve_timeframe('M15')[1]==900
def test_config_hash_changes_with_timeframe(): assert config(HostTimeframe.M5).config_hash!=config(HostTimeframe.M15).config_hash
def test_projection_uses_first_close_after_candidate():
    c=candidate();cfg=config();b=host_bar(c);p=project_candidate(c,(b,),cfg);assert p.target_host_bar_id==b.host_bar_id
def test_projection_deterministic():
    c=candidate();cfg=config();b=host_bar(c);assert project_candidate(c,(b,),cfg)==project_candidate(c,(b,),cfg)
def test_wrong_host_symbol_not_selected():
    c=candidate();cfg=config();b=host_bar(c);object.__setattr__(b,'canonical_symbol','NQ')
    with pytest.raises(Exception):project_candidate(c,(b,),cfg)
def test_projection_rejects_terminal_candidate():
    c=candidate();object.__setattr__(c,'state',__import__('fp_i06_relations.enums',fromlist=['CandidateState']).CandidateState.CHECK_WINDOW_ENDED)
    with pytest.raises(Exception):project_candidate(c,(host_bar(candidate()),),config())

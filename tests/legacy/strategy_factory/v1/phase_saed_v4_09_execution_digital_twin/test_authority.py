import copy, pytest
from .helpers import inputs,built
from saed_v4_execution_twin.authority import validate_handoff
from saed_v4_execution_twin.errors import AuthorityError,IntegrityError

def test_upstream_handoff_is_exactly_bound():
    cube,handoff,_=inputs();validate_handoff(cube,handoff)

def test_authority_escalation_fails():
    cube,handoff,_=inputs();handoff=copy.deepcopy(handoff);handoff['authority']['send_order']=True
    with pytest.raises(AuthorityError):validate_handoff(cube,handoff)

def test_cube_hash_mismatch_fails():
    cube,handoff,_=inputs();handoff=copy.deepcopy(handoff);handoff['cube_hash']='0'*64
    with pytest.raises(IntegrityError):validate_handoff(cube,handoff)

def test_output_has_no_selection_or_execution_authority():
    *_,twin=built();assert twin['authority']['select_treatment'] is False;assert twin['authority']['send_order'] is False;assert twin['shadow_replacement'] is False

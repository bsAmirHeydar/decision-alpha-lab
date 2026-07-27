import pytest
from .helpers import inputs,solve
from saed_v4_action_lattice.service import ActionLatticeService
@pytest.mark.parametrize('field',['selection_authority','execution_authority'])
def test_outputs_have_no_authority(field):
 o=solve();assert o['solver_result'][field] is False and o['action_lattice'][field] is False
@pytest.mark.parametrize('field',['select_treatment','train_model','allocate_risk','activate_runtime','send_order','network_access','use_future_outcomes','rank_by_realized_outcome'])
def test_policy_authority_leak_rejected(field):
 p,h,pol,d,r=inputs();pol['authority'][field]=True
 with pytest.raises(ValueError):ActionLatticeService().solve(package=p,handoff=h,policy_document=pol,domain_registry=d,request=r)

import pytest
from .helpers import inputs
from saed_v4_action_lattice.service import ActionLatticeService
from saed_v4_action_lattice.errors import BudgetError
@pytest.mark.parametrize(('key','value'), [('maximum_candidates',8),('maximum_feasible_nodes',8),('maximum_edges',8),('maximum_constraint_evaluations',8),('operation_budget',16)])
def test_budget_fail_closed(key,value):
 p,h,pol,d,r=inputs();pol['budget'][key]=value
 from saed_v4_action_lattice.models import LatticePolicy
 obj=LatticePolicy.from_mapping(pol);pol['policy_id']=obj.policy_id;pol['policy_hash']=obj.policy_hash;r['policy_id']=obj.policy_id;r['policy_hash']=obj.policy_hash
 from saed_v4_action_lattice.canonical import content_hash,stable_id
 seed={k:v for k,v in r.items() if k not in ('request_id','request_hash')};r['request_id']=stable_id('solverrequest',seed);r['request_hash']=content_hash(seed)
 with pytest.raises(BudgetError):ActionLatticeService().solve(package=p,handoff=h,policy_document=pol,domain_registry=d,request=r)

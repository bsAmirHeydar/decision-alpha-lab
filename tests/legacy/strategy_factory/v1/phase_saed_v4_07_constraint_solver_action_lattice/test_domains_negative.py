import copy,pytest
from .helpers import inputs
from saed_v4_action_lattice.service import ActionLatticeService
from saed_v4_action_lattice.errors import DomainError
@pytest.mark.parametrize('mutation', ['unknown_program','duplicate','missing_source','future','outcome','too_many'])
def test_domain_fail_closed(mutation):
 p,h,pol,d,r=inputs();x=d['domains'][0]
 if mutation=='unknown_program':x['program_id']='unknown'
 elif mutation=='duplicate':x['ordered_values']=['1.0','1.0']
 elif mutation=='missing_source':x['ordered_values']=['9.0','10.0']
 elif mutation=='future':x['parameter_ref']='component:entry.future_price'
 elif mutation=='outcome':x['domain_name']='realized_outcome_rank'
 else:x['ordered_values']=[str(i) for i in range(65)]
 with pytest.raises(DomainError):ActionLatticeService().solve(package=p,handoff=h,policy_document=pol,domain_registry=d,request=r)

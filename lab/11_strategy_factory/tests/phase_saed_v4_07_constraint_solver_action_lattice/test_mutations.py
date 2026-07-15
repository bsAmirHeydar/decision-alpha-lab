import copy,pytest
from helpers import solve
from saed_v4_action_lattice.validation import validate_lattice,validate_solver_result
from saed_v4_action_lattice.errors import ContractError,IntegrityError
@pytest.mark.parametrize('field',['candidate_count','feasible_count','pruned_count'])
def test_result_count_mutation_rejected(field):
 r=copy.deepcopy(solve()['solver_result']);r[field]+=1
 with pytest.raises((ContractError,IntegrityError)):validate_solver_result(r)
@pytest.mark.parametrize('mutation',['dangling','self_loop','reverse','two_step','authority'])
def test_lattice_mutations_rejected(mutation):
 l=copy.deepcopy(solve()['action_lattice'])
 if mutation=='dangling':l['edges'][0]['target_node_id']='missing'
 elif mutation=='self_loop':l['edges'][0]['target_node_id']=l['edges'][0]['source_node_id']
 elif mutation=='reverse':
  e=next(e for e in l['edges'] if e['edge_kind']=='atomic_parameter_step');e['source_node_id'],e['target_node_id']=e['target_node_id'],e['source_node_id']
 elif mutation=='two_step':
  e=next(e for e in l['edges'] if e['edge_kind']=='atomic_parameter_step');e['mutation']['to_index']=e['mutation']['from_index']+2
 else:l['selection_authority']=True
 with pytest.raises((ContractError,IntegrityError)):validate_lattice(l)

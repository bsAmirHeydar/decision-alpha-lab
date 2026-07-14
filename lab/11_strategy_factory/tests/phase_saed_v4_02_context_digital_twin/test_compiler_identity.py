import copy,pytest
from saed_v4_context_twin.compiler import compile_twin
from saed_v4_context_twin.errors import ContractError,IdentityError

def test_deterministic(context_spec,seed):
 a=compile_twin(context_spec,seed);b=compile_twin(copy.deepcopy(context_spec),copy.deepcopy(seed));assert a.twin_id==b.twin_id and a.semantic_hash==b.semantic_hash

def test_order_independent(context_spec,seed):
 x=copy.deepcopy(context_spec);x['ontology_terms'].reverse();x['observables'].reverse();x['hypotheses'].reverse();x['transition_rules'].reverse();assert compile_twin(x,seed).semantic_hash==compile_twin(context_spec,seed).semantic_hash

def test_seed_mismatch(context_spec,seed):
 s=dict(seed);s['context_specification_artifact_id']='bad'
 with pytest.raises(IdentityError):compile_twin(context_spec,s)

def test_unknown_field(context_spec,seed):
 c=dict(context_spec);c['x']=1
 with pytest.raises(ContractError):compile_twin(c,seed)

def test_authority_denied(context_spec,seed):
 a=compile_twin(context_spec,seed).authority;assert a.read_ucee_truth and a.compile_twin and not a.mutate_ucee_truth and not a.select_treatment and not a.allocate_risk and not a.activate_runtime and not a.send_order and not a.network_access

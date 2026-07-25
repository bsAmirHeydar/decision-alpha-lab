from dataclasses import replace
import pytest
from saed_v4_treatment_dsl.authority import validate_authority
from saed_v4_treatment_dsl.catalog import institutional_policy,institutional_registry
from saed_v4_treatment_dsl.errors import AuthorityError,RegistryError
from saed_v4_treatment_dsl.registry import validate_policy,validate_registry

def test_registry_and_policy_are_valid():
 p=institutional_policy();r=institutional_registry();validate_policy(p);validate_registry(r,p)
def test_registry_exact_keys_are_unique():
 r=institutional_registry(); keys=[x.exact_key for x in r.primitives]; assert len(keys)==len(set(keys))
@pytest.mark.parametrize('field',['mutate_ucee_truth','mutate_hypergraph','generate_unbounded_actions','solve_action_lattice','select_treatment','train_model','allocate_risk','activate_runtime','send_order','network_access'])
def test_forbidden_authority_rejected(field):
 r=institutional_registry(); b=replace(r.authority,**{field:True})
 with pytest.raises(AuthorityError): validate_authority(b)
@pytest.mark.parametrize('field',['read_hypergraph','read_handoff','define_finite_dsl','canonicalize_program','validate_program','bind_external_descriptor','replay_and_diff'])
def test_required_authority_cannot_be_removed(field):
 r=institutional_registry(); b=replace(r.authority,**{field:False})
 with pytest.raises(AuthorityError): validate_authority(b)
def test_policy_budgets_fail_closed():
 p=replace(institutional_policy(),maximum_programs=0)
 with pytest.raises(RegistryError):validate_policy(p)

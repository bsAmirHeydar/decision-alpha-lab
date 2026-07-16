import pytest
from saed_v4_causal_treatment_policy_value.contracts import TreatmentRegistry,OutcomeSpec,IdentificationPlan,EstimatorSpec,PolicySpec,ComputeExposureBudget
from saed_v4_causal_treatment_policy_value.errors import ContractError

def test_treatment_registry(load,ex):
 r=TreatmentRegistry.from_mapping(load(f'{ex}/reference_treatment_registry.json'));assert r.frozen and not r.runtime_selectable and len(r.treatments)==4

def test_outcome_spec(load,ex):
 o=OutcomeSpec.from_mapping(load(f'{ex}/reference_outcome_spec.json'));assert o.cost_adjusted and not o.protected_final_role

def test_identification_plan(load,ex):
 p=IdentificationPlan.from_mapping(load(f'{ex}/reference_identification_plan.json'));assert p.future_training_forbidden and p.sibling_split_forbidden and p.cross_fit_folds==4

@pytest.mark.parametrize('index',range(5))
def test_estimators(load,ex,index):
 e=EstimatorSpec.from_mapping(load(f'{ex}/reference_estimator_catalog.json')[index]);assert e.supports_multitreatment

@pytest.mark.parametrize('index',range(7))
def test_policies(load,ex,index):
 p=PolicySpec.from_mapping(load(f'{ex}/reference_policy_catalog.json')[index]);assert p.evaluation_only and p.preserve_manual_fallback

def test_budget(load,ex):
 b=ComputeExposureBudget.from_mapping(load(f'{ex}/reference_compute_exposure_budget.json'));assert b.protected_evidence_exposure_limit==0 and b.hidden_evaluation_query_limit==0

@pytest.mark.parametrize('field,value',[
 ('runtime_selectable',True),('finite',False),('frozen',False)])
def test_treatment_registry_mutations_fail(load,ex,field,value):
 x=load(f'{ex}/reference_treatment_registry.json');x[field]=value
 with pytest.raises(ContractError):TreatmentRegistry.from_mapping(x)

def test_unknown_field_fails(load,ex):
 x=load(f'{ex}/reference_outcome_spec.json');x['unknown']=1
 with pytest.raises(ContractError):OutcomeSpec.from_mapping(x)

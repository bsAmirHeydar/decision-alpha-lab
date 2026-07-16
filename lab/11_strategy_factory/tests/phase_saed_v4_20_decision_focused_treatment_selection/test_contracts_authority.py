import copy,pytest
from saed_v4_decision_focused_treatment_selection.contracts import TreatmentUniverseContract,DecisionProblemContract,UtilityContract,ConstraintContract,RiskContract,SelectionPolicyContract,SelectionBudget
from saed_v4_decision_focused_treatment_selection.errors import ContractError,AuthorityError
from saed_v4_decision_focused_treatment_selection.authority import assert_operation,boundary_record,ALLOWED,FORBIDDEN

def test_all_reference_contracts_parse(config):
 TreatmentUniverseContract.from_mapping(config['treatment_universe']);DecisionProblemContract.from_mapping(config['decision_problem']);UtilityContract.from_mapping(config['utility']);ConstraintContract.from_mapping(config['constraints']);RiskContract.from_mapping(config['risk']);SelectionPolicyContract.from_mapping(config['selection_policy']);SelectionBudget.from_mapping(config['budget'])
@pytest.mark.parametrize('name,key',[
 ('treatment_universe','closed_world'),('treatment_universe','runtime_mutation_allowed'),('decision_problem','future_suffix_forbidden'),('decision_problem','protected_evidence_forbidden'),('constraints','proof_required'),('constraints','manual_approval_required'),('constraints','hard_fail_to_skip'),('selection_policy','baseline_preservation'),('selection_policy','pareto_required'),('selection_policy','deterministic')])
def test_safety_boolean_mutation_rejected(config,name,key):
 x=copy.deepcopy(config[name]);x[key]=not x[key]
 with pytest.raises(ContractError):
  {'treatment_universe':TreatmentUniverseContract,'decision_problem':DecisionProblemContract,'constraints':ConstraintContract,'selection_policy':SelectionPolicyContract}[name].from_mapping(x)
@pytest.mark.parametrize('name,cls',[('treatment_universe',TreatmentUniverseContract),('decision_problem',DecisionProblemContract),('utility',UtilityContract),('constraints',ConstraintContract),('risk',RiskContract),('selection_policy',SelectionPolicyContract),('budget',SelectionBudget)])
def test_unknown_fields_rejected(config,name,cls):
 x=copy.deepcopy(config[name]);x['unknown_field']=1
 with pytest.raises(ContractError):cls.from_mapping(x)
@pytest.mark.parametrize('op',sorted(ALLOWED))
def test_allowed_operations(op):assert assert_operation(op)
@pytest.mark.parametrize('op',sorted(FORBIDDEN))
def test_forbidden_operations(op):
 with pytest.raises(AuthorityError):assert_operation(op)
def test_boundary_is_non_authoritative():
 b=boundary_record();assert b['research_reference_only'];assert not any(b[k] for k in ['real_policy_value_claim_authority','production_treatment_selection_authority','decision_authority','promotion_authority','runtime_authority','execution_authority','production_authority'])

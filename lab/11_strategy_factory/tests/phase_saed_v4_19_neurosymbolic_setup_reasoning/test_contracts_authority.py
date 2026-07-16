import pytest
from saed_v4_neurosymbolic_setup_reasoning.contracts import OntologyContract,PredicateRegistry,TemporalLogicContract,RuleGrammar,ReasoningBudget,DecisionEnvelopeContract
from saed_v4_neurosymbolic_setup_reasoning.authority import assert_operation,boundary_record
from saed_v4_neurosymbolic_setup_reasoning.errors import ContractError,AuthorityError

def test_contracts(load,ex):
 OntologyContract.from_mapping(load(ex+'/ONTOLOGY_CONTRACT.JSON'));PredicateRegistry.from_mapping(load(ex+'/PREDICATE_REGISTRY.JSON'));TemporalLogicContract.from_mapping(load(ex+'/TEMPORAL_LOGIC_CONTRACT.JSON'));RuleGrammar.from_mapping(load(ex+'/RULE_GRAMMAR.JSON'));ReasoningBudget.from_mapping(load(ex+'/REASONING_BUDGET.JSON'));DecisionEnvelopeContract.from_mapping(load(ex+'/DECISION_ENVELOPE_CONTRACT.JSON'))
@pytest.mark.parametrize('op',['read_immutable_v4_18_handoff','freeze_ontology','register_predicates','evaluate_known_time_facts','evaluate_temporal_constraints','run_bounded_forward_chaining','compute_differentiable_logic_scores','project_to_approved_action_lattice','synthesize_bounded_rules','run_symbolic_regression_reference','search_synthetic_counterexamples','compare_neural_symbolic_outputs','build_proof_envelope','preserve_skip_and_manual_baselines','register_research_checkpoint','reproduce_golden','build_v4_20_handoff'])
def test_allowed(op):assert assert_operation(op)
@pytest.mark.parametrize('op',['mutate_v4_18_evidence','read_protected_final_evidence','execute_dynamic_code','expand_runtime_ontology','assert_real_mechanism','assert_real_policy_value','select_live_treatment','allocate_risk','sign_promotion','compile_runtime','activate_runtime','access_live_credentials','send_order'])
def test_forbidden(op):
 with pytest.raises(AuthorityError):assert_operation(op)
def test_boundary():
 b=boundary_record();assert b['research_reference_only'] and not any(b[k] for k in ['decision_authority','promotion_authority','runtime_authority','execution_authority','production_authority'])
def test_unknown_field(load,ex):
 x=load(ex+'/ONTOLOGY_CONTRACT.JSON');x['unknown']=1
 with pytest.raises(ContractError):OntologyContract.from_mapping(x)

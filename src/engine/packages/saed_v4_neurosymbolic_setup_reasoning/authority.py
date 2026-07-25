from .errors import AuthorityError
ALLOWED={
 'read_immutable_v4_18_handoff','freeze_ontology','register_predicates','evaluate_known_time_facts','evaluate_temporal_constraints',
 'run_bounded_forward_chaining','compute_differentiable_logic_scores','project_to_approved_action_lattice','synthesize_bounded_rules',
 'run_symbolic_regression_reference','search_synthetic_counterexamples','compare_neural_symbolic_outputs','build_proof_envelope',
 'preserve_skip_and_manual_baselines','register_research_checkpoint','reproduce_golden','build_v4_20_handoff'
}
FORBIDDEN={
 'mutate_v4_18_evidence','read_protected_final_evidence','execute_dynamic_code','expand_runtime_ontology','assert_real_mechanism',
 'assert_real_policy_value','select_live_treatment','allocate_risk','sign_promotion','compile_runtime','activate_runtime','access_live_credentials','send_order'
}
def assert_operation(op):
    if op in FORBIDDEN:raise AuthorityError(f'forbidden operation: {op}')
    if op not in ALLOWED:raise AuthorityError(f'unknown operation: {op}')
    return True
def boundary_record():
    return {'phase':'SAED_V4_19','research_reference_only':True,'claim_ceiling':'synthetic_proof_carrying_reasoning_not_real','allowed_operations':sorted(ALLOWED),'forbidden_operations':sorted(FORBIDDEN),'real_mechanism_claim_authority':False,'production_treatment_selection_authority':False,'decision_authority':False,'promotion_authority':False,'runtime_authority':False,'execution_authority':False,'production_authority':False}

from .errors import AuthorityError
ALLOWED={
 'read_frozen_v4_16_evidence','build_synthetic_causal_benchmark','register_observed_variables','register_declared_environments',
 'fit_association_baseline','discover_reference_candidate_graph','audit_temporal_precedence','audit_conditional_independence',
 'audit_invariance','fit_reference_structural_equations','compute_reference_orthogonal_score','run_negative_controls',
 'run_hidden_confounder_sensitivity','run_environment_permutation','run_transport_support_audit','tier_reference_claims',
 'register_research_checkpoint','reproduce_golden','build_v4_18_handoff'
}
FORBIDDEN={
 'mutate_v4_16_evidence','consume_protected_final_evidence','assert_real_causality','identify_unobserved_cause_as_fact',
 'estimate_production_treatment_effect','rank_treatments','select_treatment','allocate_risk','sign_promotion',
 'compile_runtime','activate_runtime','access_live_credentials','send_order'
}
def assert_operation(operation):
    if operation in FORBIDDEN:raise AuthorityError(f'forbidden operation: {operation}')
    if operation not in ALLOWED:raise AuthorityError(f'unknown operation: {operation}')
    return True
def boundary_record():
    return {'phase':'SAED_V4_17','research_reference_only':True,'claim_ceiling':'mechanism_compatible_synthetic_not_causal','allowed_operations':sorted(ALLOWED),'forbidden_operations':sorted(FORBIDDEN),'causal_claim_authority':False,'decision_authority':False,'promotion_authority':False,'runtime_authority':False,'execution_authority':False,'production_authority':False}

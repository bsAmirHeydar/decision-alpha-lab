from .errors import AuthorityError
ALLOWED={
 'read_immutable_v4_20_selection','freeze_ambiguity_set','compile_synthetic_scenarios','enumerate_bounded_allocations',
 'compute_synthetic_robust_utility','compute_synthetic_regret','compute_synthetic_cvar','solve_reference_robust_program',
 'preserve_manual_and_skip_baselines','run_synthetic_sensitivity','run_synthetic_adversary','build_robust_certificate',
 'register_research_checkpoint','reproduce_golden','build_v4_22_handoff'
}
FORBIDDEN={
 'mutate_upstream_evidence','read_protected_final_evidence','learn_from_hidden_evaluation','assert_real_policy_value','assert_real_alpha',
 'select_live_treatment','allocate_live_risk','sign_promotion','compile_runtime','activate_runtime','access_live_credentials','send_order'
}
def assert_operation(op):
    if op in FORBIDDEN: raise AuthorityError(f'forbidden operation: {op}')
    if op not in ALLOWED: raise AuthorityError(f'unknown operation: {op}')
    return True
def boundary_record():
    return {'phase':'SAED_V4_21','research_reference_only':True,'claim_ceiling':'synthetic_robust_optimization_not_real_policy_value','allowed_operations':sorted(ALLOWED),'forbidden_operations':sorted(FORBIDDEN),'real_policy_value_claim_authority':False,'production_treatment_selection_authority':False,'risk_allocation_authority':False,'promotion_authority':False,'runtime_authority':False,'execution_authority':False,'production_authority':False}

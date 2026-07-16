from .errors import AuthorityError
ALLOWED={
 'read_immutable_v4_18_policy_value','read_immutable_v4_19_proof_envelope','freeze_treatment_universe','compile_action_mask',
 'compute_synthetic_utility','compute_synthetic_risk','compute_synthetic_regret','construct_pareto_frontier','rank_approved_treatments',
 'produce_set_valued_selection','calibrate_reference_scores','apply_abstention','preserve_skip_and_manual_baselines',
 'build_selection_certificate','register_research_checkpoint','reproduce_golden','build_v4_21_handoff'
}
FORBIDDEN={
 'mutate_upstream_evidence','read_protected_final_evidence','assert_real_policy_value','assert_real_alpha','select_live_treatment',
 'allocate_risk','sign_promotion','compile_runtime','activate_runtime','access_live_credentials','send_order'
}
def assert_operation(op):
    if op in FORBIDDEN:raise AuthorityError(f'forbidden operation: {op}')
    if op not in ALLOWED:raise AuthorityError(f'unknown operation: {op}')
    return True
def boundary_record():
    return {'phase':'SAED_V4_20','research_reference_only':True,'claim_ceiling':'synthetic_decision_selection_not_real_policy_value','allowed_operations':sorted(ALLOWED),'forbidden_operations':sorted(FORBIDDEN),'real_policy_value_claim_authority':False,'production_treatment_selection_authority':False,'decision_authority':False,'promotion_authority':False,'runtime_authority':False,'execution_authority':False,'production_authority':False}

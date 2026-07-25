from .errors import AuthorityError
ALLOWED={
 'read_frozen_v4_17_evidence','freeze_synthetic_treatment_universe','build_synthetic_treatment_dataset','construct_chronological_cluster_folds',
 'fit_reference_propensity','audit_overlap','fit_cross_fitted_nuisance','estimate_synthetic_ate','estimate_synthetic_cate','rank_synthetic_treatments',
 'evaluate_synthetic_policy','run_negative_controls','run_propensity_sensitivity','run_unmeasured_confounding_sensitivity','run_cost_tail_transport_stress',
 'preserve_baselines','register_research_checkpoint','reproduce_golden','build_v4_19_handoff'
}
FORBIDDEN={
 'mutate_v4_17_evidence','consume_protected_final_evidence','assert_real_treatment_effect','assert_real_policy_value','rank_production_treatments',
 'select_live_treatment','allocate_risk','sign_promotion','compile_runtime','activate_runtime','access_live_credentials','send_order'
}
def assert_operation(operation):
    if operation in FORBIDDEN:raise AuthorityError(f'forbidden operation: {operation}')
    if operation not in ALLOWED:raise AuthorityError(f'unknown operation: {operation}')
    return True
def boundary_record():
    return {'phase':'SAED_V4_18','research_reference_only':True,'claim_ceiling':'synthetic_treatment_and_policy_value_not_real','allowed_operations':sorted(ALLOWED),'forbidden_operations':sorted(FORBIDDEN),'real_causal_claim_authority':False,'production_treatment_ranking_authority':False,'decision_authority':False,'promotion_authority':False,'runtime_authority':False,'execution_authority':False,'production_authority':False}

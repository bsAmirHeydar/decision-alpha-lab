from .errors import AuthorityError
ALLOWED={'read_frozen_v4_15_fusion_features','read_frozen_v4_15_registry','build_synthetic_survival_dataset','fit_reference_survival_models','fit_reference_distribution_models','estimate_synthetic_hazards','estimate_synthetic_distributions','calibrate_reference_outputs','run_tail_stress_suite','register_research_checkpoint','reproduce_golden','build_v4_17_handoff'}
FORBIDDEN={'mutate_v4_15_evidence','use_protected_final_evidence','predict_live_outcomes','rank_treatments','select_treatment','allocate_risk','sign_promotion','compile_runtime','activate_runtime','access_live_credentials','send_order'}
def assert_operation(operation):
    if operation in FORBIDDEN:raise AuthorityError(f'forbidden operation: {operation}')
    if operation not in ALLOWED:raise AuthorityError(f'unknown operation: {operation}')
    return True
def boundary_record():
    return {'phase':'SAED_V4_16','research_reference_only':True,'allowed_operations':sorted(ALLOWED),'forbidden_operations':sorted(FORBIDDEN),'decision_authority':False,'promotion_authority':False,'runtime_authority':False,'execution_authority':False,'production_authority':False}

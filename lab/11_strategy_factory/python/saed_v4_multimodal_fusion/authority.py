from .errors import AuthorityError
ALLOWED={'read_frozen_view_package','read_frozen_foundation_features','encode_view_envelopes','evaluate_reference_fusion','audit_missing_view_subsets','register_research_checkpoint','handoff_frozen_fusion_features'}
FORBIDDEN={'mutate_context_truth','mutate_upstream','predict_outcome','rank_treatment','select_treatment','allocate_risk','activate_runtime','send_order','remote_inference','online_learning','treat_attribution_as_causal'}
def assert_operation(op):
    if op not in ALLOWED: raise AuthorityError(f'operation forbidden: {op}')
    return True
def boundary_record():
    return {'phase':'SAED_V4_15','capability_tier':'GOVERNED_CHALLENGER','allowed_operations':sorted(ALLOWED),'forbidden_operations':sorted(FORBIDDEN),'decision_authority':False,'runtime_authority':False,'execution_authority':False,'attribution_is_causal':False,'fail_closed_fallback':'late_mean_baseline_or_abstain'}

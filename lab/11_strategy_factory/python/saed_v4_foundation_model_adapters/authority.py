from .errors import AuthorityError
FORBIDDEN={'predict_outcome','rank_treatment','select_treatment','allocate_risk','activate_runtime','send_order','mutate_upstream','remote_inference','online_learning'}
ALLOWED={'read_frozen_graph_embeddings','materialize_reference_features','evaluate_self_supervised_objectives','register_research_checkpoint','handoff_frozen_features'}
def assert_operation(op):
    if op in FORBIDDEN or op not in ALLOWED: raise AuthorityError(f'operation forbidden: {op}')
    return True
def boundary_record():
    return {'phase':'SAED_V4_14','capability_tier':'GOVERNED_CHALLENGER','allowed_operations':sorted(ALLOWED),'forbidden_operations':sorted(FORBIDDEN),'decision_authority':False,'runtime_authority':False,'execution_authority':False,'fail_closed_fallback':'native_linear_baseline_or_abstain'}

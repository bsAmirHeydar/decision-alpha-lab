from .errors import AuthorityError
AUTHORITY={
 'read_frozen_v4_05_hypergraph':True,'read_frozen_v4_12_sequence_registry':True,
 'read_frozen_v4_12_distilled_states':True,'compile_known_time_graph_views':True,
 'build_reference_graph_hypergraph_challengers':True,'fit_self_supervised_readouts':True,
 'emit_research_checkpoint':True,'emit_v4_14_handoff':True,
 'mutate_v4_05_graph':False,'mutate_v4_12_artifacts':False,'infer_new_canonical_relations':False,
 'use_outcome_cube_as_input':False,'use_execution_twin_as_input':False,'use_protected_final':False,
 'use_prospective_shadow_live':False,'predict_trade_outcomes':False,'rank_treatments':False,
 'select_treatment':False,'allocate_risk':False,'activate_runtime':False,'send_order':False,
}
def assert_authority(candidate:dict)->None:
    unknown=set(candidate)-set(AUTHORITY)
    if unknown: raise AuthorityError(f'unknown authority keys: {sorted(unknown)}')
    for key,allowed in AUTHORITY.items():
        if not allowed and candidate.get(key) is True: raise AuthorityError(f'forbidden authority requested: {key}')
def boundary_record()->dict:
    return {'phase':'SAED_V4_13','authority':'reference_synthetic_only','capabilities':dict(AUTHORITY),'decision_authority':False,'runtime_authority':False,'execution_authority':False,'fail_closed':True}

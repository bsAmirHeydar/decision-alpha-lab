from .errors import AuthorityError
AUTHORITY={
 'read_frozen_v4_11_tokenizer':True,'read_frozen_v4_11_encoder':True,
 'compile_known_time_sequences':True,'build_reference_sequence_challengers':True,
 'fit_self_supervised_readouts':True,'evaluate_streaming_parity':True,
 'emit_research_checkpoint':True,'emit_v4_13_handoff':True,
 'mutate_v4_11_artifacts':False,'use_outcome_cube_as_input':False,
 'use_execution_twin_as_input':False,'use_protected_final':False,
 'use_prospective_shadow_live':False,'fine_tune_real_or_protected_data':False,
 'predict_trade_outcomes':False,'rank_treatments':False,'select_treatment':False,
 'allocate_risk':False,'activate_runtime':False,'send_order':False,
}

def assert_authority(candidate:dict)->None:
    unknown=set(candidate)-set(AUTHORITY)
    if unknown: raise AuthorityError(f'unknown authority keys: {sorted(unknown)}')
    for key,allowed in AUTHORITY.items():
        if not allowed and candidate.get(key) is True: raise AuthorityError(f'forbidden authority requested: {key}')

def boundary_record()->dict:
    return {'phase':'SAED_V4_12','authority':'reference_synthetic_only','capabilities':dict(AUTHORITY),'decision_authority':False,'runtime_authority':False,'execution_authority':False,'fail_closed':True}

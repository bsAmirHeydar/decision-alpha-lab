from .errors import AuthorityError
ALLOWED_EVIDENCE_ROLES={'development','validation','test','prospective'}
PROHIBITED_OPERATIONS={'train_model','select_treatment','rank_treatments','allocate_risk','activate_runtime','send_order','mutate_action_lattice','use_future_information_at_decision_time'}
AUTHORITY_BOUNDARY={
 'read_frozen_action_lattice':True,'read_v4_07_handoff':True,'evaluate_deferred_known_time_predicates':True,
 'compile_executable_path_specs':True,'simulate_counterfactual_paths':True,'build_executable_path_outcome_cube':True,
 'emit_v4_09_handoff':True,'train_model':False,'select_treatment':False,'rank_treatments':False,
 'allocate_risk':False,'activate_runtime':False,'send_order':False,'mutate_action_lattice':False,
 'use_future_information_at_decision_time':False,'network_access':False}
def assert_evidence_role(role:str)->None:
    if role not in ALLOWED_EVIDENCE_ROLES: raise AuthorityError(f'evidence role not permitted: {role}')
def assert_operation(operation:str)->None:
    if operation in PROHIBITED_OPERATIONS or not AUTHORITY_BOUNDARY.get(operation,False): raise AuthorityError(f'operation prohibited: {operation}')

from __future__ import annotations
from datetime import datetime
from .canonical import verify_embedded_digest,with_digest
from .errors import ContractError
def dt(v:str)->datetime: return datetime.fromisoformat(v.replace('Z','+00:00'))
def validate_request(req:dict,binding:dict)->dict:
    if not verify_embedded_digest(req,'pilot_request_digest'): raise ContractError('ACL14_REQUEST_DIGEST_INVALID')
    if req.get('schema_version')!='1.0.0': raise ContractError('ACL14_REQUEST_VERSION_INVALID')
    required=['pilot_request_id','source_assessment_run_id','context_id','context_version','context_title','doctrine_summary','evidence_classification','real_context_evidence_present','owner_approvals','data_sources','data_mapping','availability_semantics','pilot_period','evaluation_rules','setup_search_space','support_targets','stop_conditions','failure_conditions','operator_roles','non_capital_boundary']
    if any(k not in req for k in required): raise ContractError('ACL14_REQUEST_FIELD_MISSING')
    if req['source_assessment_run_id']!=binding['assessment_run_id']: raise ContractError('ACL14_SOURCE_RUN_MISMATCH')
    if not req['context_id'] or not req['context_version'] or not req['doctrine_summary'].strip(): raise ContractError('ACL14_CONTEXT_IDENTITY_OR_DOCTRINE_MISSING')
    if req['evidence_classification'] not in {'APPROVED_REAL_CONTEXT','REFERENCE_REPRESENTATIVE_NOT_REAL'}: raise ContractError('ACL14_EVIDENCE_CLASSIFICATION_INVALID')
    if req['synthetic_or_reference_reuse_as_real'] is not False: raise ContractError('ACL14_SYNTHETIC_REUSE_AS_REAL_DENIED')
    if req['availability_semantics'].get('future_data_allowed') is not False: raise ContractError('ACL14_FUTURE_DATA_AUTHORITY_DENIED')
    if req['setup_search_space'].get('dynamic_generation_allowed') is not False or req['setup_search_space'].get('ai_generation_allowed') is not False: raise ContractError('ACL14_DYNAMIC_SEARCH_EXPANSION_DENIED')
    if req['setup_search_space'].get('frozen') is not True: raise ContractError('ACL14_SEARCH_SPACE_NOT_FROZEN')
    if req['evaluation_rules'].get('frozen') is not True or req['evaluation_rules'].get('post_outcome_change_allowed') is not False: raise ContractError('ACL14_EVALUATION_RULES_NOT_FROZEN')
    if not req['stop_conditions'] or not req['failure_conditions']: raise ContractError('ACL14_STOP_OR_FAILURE_CONDITIONS_MISSING')
    period=req['pilot_period']; start,end,pre=dt(period['start_at']),dt(period['end_at']),dt(period['precommitted_at'])
    if not pre<start<end: raise ContractError('ACL14_PILOT_PERIOD_INVALID')
    if req['non_capital_boundary'].get('pilot_mode')!='NO_SEND_PROSPECTIVE_OBSERVATION': raise ContractError('ACL14_PILOT_MODE_INVALID')
    denied=['order_submission_allowed','broker_connection_allowed','runtime_activation_allowed','capital_allocation_allowed']
    if any(req['non_capital_boundary'].get(k) is not False for k in denied): raise ContractError('ACL14_NON_CAPITAL_BOUNDARY_INVALID')
    roles={x.get('role') for x in req['operator_roles']}
    if not {'CONTEXT_OWNER','PILOT_REVIEWER','DATA_CUSTODIAN'}.issubset(roles): raise ContractError('ACL14_OPERATOR_ROLES_INCOMPLETE')
    return with_digest({'schema_version':'1.0.0','pilot_request_id':req['pilot_request_id'],'context_id':req['context_id'],'context_version':req['context_version'],'evidence_classification':req['evidence_classification'],'real_context_evidence_present':req['real_context_evidence_present'],'request_valid':True,'known_time_contract_present':True,'search_space_frozen':True,'evaluation_rules_frozen':True,'non_capital_boundary_valid':True,'synthetic_reuse_as_real':False},'input_validation_digest')

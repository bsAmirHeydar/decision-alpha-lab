from __future__ import annotations
from .canonical import stable_id,with_digest
from .policies import GATE_IDS
def result(gate_id:str,status:str,reasons:list[str],evidence:list[str])->dict:
    return with_digest({'schema_version':'1.0.0','gate_id':gate_id,'status':status,'reason_codes':reasons,'evidence_digests':evidence},'gate_result_digest')
def assess(binding:dict,req:dict,contracts:dict)->dict:
    real=req['evidence_classification']=='APPROVED_REAL_CONTEXT' and req['real_context_evidence_present'] is True
    approved_roles={x['owner_role'] for x in req['owner_approvals'] if x.get('approval_status')=='APPROVED'}
    independent_owner={'CONTEXT_OWNER','PILOT_REVIEWER'}.issubset(approved_roles)
    doctrine=any(x.get('owner_role')=='CONTEXT_OWNER' and x.get('approval_status')=='APPROVED' for x in req['owner_approvals']) and bool(req['doctrine_summary'].strip())
    real_sources=bool(req['data_sources']) and all(x.get('real_data') is True and x.get('approved') is True for x in req['data_sources'])
    mapping=req['data_mapping']['mapping_complete'] is True
    availability=req['availability_semantics']['known_time_enforced'] is True and req['availability_semantics']['future_data_allowed'] is False
    externally=req['availability_semantics']['externally_verified'] is True
    operator_ids=[x['operator_id'] for x in req['operator_roles']]
    separated=len(operator_ids)==len(set(operator_ids)) and len(set(operator_ids))>=3
    vals={
      'ACL13_PACKAGE_INTEGRITY':('SATISFIED',['ACL13_PACKAGE_VERIFIED'],[binding['binding_digest']]),
      'ACL13_PILOT_DESIGN_ELIGIBLE':('SATISFIED',['ACL13_PILOT_DESIGN_ALLOWED'],[binding['assessment_result_digest']]),
      'REAL_CONTEXT_IDENTITY':(('SATISFIED' if real else 'UNSATISFIED'),(['APPROVED_REAL_CONTEXT_PRESENT'] if real else ['REAL_CONTEXT_EVIDENCE_REQUIRED']),[]),
      'INDEPENDENT_OWNER_APPROVAL':(('SATISFIED' if independent_owner else 'UNKNOWN'),(['INDEPENDENT_OWNER_APPROVAL_PRESENT'] if independent_owner else ['REAL_OWNER_APPROVAL_MISSING']),[contracts['owner']['owner_approval_bundle_digest']]),
      'DOCTRINE_APPROVAL':(('SATISFIED' if doctrine else 'UNKNOWN'),(['DOCTRINE_APPROVED'] if doctrine else ['DOCTRINE_APPROVAL_MISSING']),[contracts['owner']['owner_approval_bundle_digest']]),
      'REAL_DATA_SOURCE_APPROVAL':(('SATISFIED' if real_sources else 'UNKNOWN'),(['REAL_DATA_SOURCES_APPROVED'] if real_sources else ['REAL_DATA_SOURCE_APPROVAL_MISSING']),[]),
      'DATA_MAPPING_COMPLETE':(('SATISFIED' if mapping else 'UNSATISFIED'),(['DATA_MAPPING_COMPLETE'] if mapping else ['DATA_MAPPING_INCOMPLETE']),[contracts['mapping']['data_mapping_contract_digest']]),
      'AVAILABILITY_SEMANTICS_COMPLETE':(('SATISFIED' if availability and externally else 'UNKNOWN'),(['AVAILABILITY_SEMANTICS_VERIFIED'] if availability and externally else ['AVAILABILITY_EXTERNAL_VERIFICATION_MISSING']),[contracts['availability']['availability_contract_digest']]),
      'KNOWN_TIME_GUARD':(('SATISFIED' if availability else 'UNSATISFIED'),(['KNOWN_TIME_GUARD_FROZEN'] if availability else ['KNOWN_TIME_GUARD_INVALID']),[contracts['availability']['availability_contract_digest']]),
      'PILOT_PERIOD_PRECOMMITTED':('SATISFIED',['PILOT_PERIOD_PRECOMMITTED'],[contracts['contract']['pilot_contract_digest']]),
      'EVALUATION_RULES_FROZEN':('SATISFIED',['EVALUATION_RULES_FROZEN'],[contracts['evaluation']['evaluation_freeze_digest']]),
      'SETUP_SEARCH_SPACE_FROZEN':('SATISFIED',['SETUP_SEARCH_SPACE_FROZEN'],[contracts['search']['search_space_freeze_digest']]),
      'SUPPORT_TARGETS_PRECOMMITTED':('SATISFIED',['SUPPORT_TARGETS_PRECOMMITTED'],[contracts['support']['support_contract_digest']]),
      'STOP_CONDITIONS_FROZEN':('SATISFIED',['STOP_CONDITIONS_FROZEN'],[contracts['stop']['stop_contract_digest']]),
      'FAILURE_CONDITIONS_FROZEN':('SATISFIED',['FAILURE_CONDITIONS_FROZEN'],[contracts['failure']['failure_contract_digest']]),
      'NON_CAPITAL_BOUNDARY':('SATISFIED',['NON_CAPITAL_BOUNDARY_ENFORCED'],[contracts['boundary']['non_capital_boundary_digest']]),
      'SYNTHETIC_REUSE_DENIED':('SATISFIED',['SYNTHETIC_REUSE_AS_REAL_DENIED'],[]),
      'PROSPECTIVE_EVIDENCE_NOT_INVENTED':('SATISFIED',['NO_PROSPECTIVE_OUTCOMES_PRESENT'],[]),
      'SECURITY_STATUS_PRESERVED':('SATISFIED',['ACL13_SECURITY_STATUS_PRESERVED'],[binding['binding_digest']]),
      'RUNTIME_AUTHORITY_DENIED':('SATISFIED',['RUNTIME_AUTHORITY_DENIED'],[]),
      'LIVE_ORDER_AUTHORITY_DENIED':('SATISFIED',['LIVE_ORDER_AUTHORITY_DENIED'],[]),
      'CAPITAL_AUTHORITY_DENIED':('SATISFIED',['CAPITAL_AUTHORITY_DENIED'],[]),
      'OPERATOR_SEPARATION':(('SATISFIED' if separated else 'UNSATISFIED'),(['OPERATOR_SEPARATION_PRESENT'] if separated else ['OPERATOR_SEPARATION_INVALID']),[]),
      'AUDIT_AND_PROVENANCE':('SATISFIED',['AUDIT_AND_PROVENANCE_REQUIRED'],[contracts['contract']['pilot_contract_digest']]),
    }
    rows=[result(g,*vals[g]) for g in GATE_IDS]
    counts={s:sum(1 for x in rows if x['status']==s) for s in ['SATISFIED','UNSATISFIED','UNKNOWN','NOT_APPLICABLE']}
    ready=counts['UNSATISFIED']==0 and counts['UNKNOWN']==0
    return with_digest({'schema_version':'1.0.0','readiness_matrix_id':stable_id('PILOTREADY',req['pilot_request_id'],length=28),'pilot_request_id':req['pilot_request_id'],'gate_count':len(rows),'gates':rows,'status_counts':counts,'unknown_blocks_readiness':True,'all_required_gates_satisfied':ready,'pilot_ready_non_capital':ready},'readiness_matrix_digest')

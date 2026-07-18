from __future__ import annotations
from .canonical import stable_id,with_digest
def issue(req:dict,readiness:dict,decided_at:str)->dict:
    if readiness['pilot_ready_non_capital']:
        state='PILOT_READY_NON_CAPITAL_NOT_EXECUTED'; reasons=['ALL_PILOT_READINESS_GATES_SATISFIED','NON_CAPITAL_PILOT_READY','PILOT_EXECUTION_NOT_PERFORMED','VALIDATION_NOT_PERFORMED']
    else:
        state='PILOT_CONTRACT_AUTHORED_REAL_EVIDENCE_REQUIRED'; reasons=['PILOT_CONTRACT_AUTHORED','REAL_CONTEXT_EVIDENCE_REQUIRED','UNKNOWN_OR_UNSATISFIED_GATES_BLOCK_READINESS','PILOT_EXECUTION_NOT_AUTHORIZED','VALIDATION_NOT_PERFORMED']
    body={'schema_version':'1.0.0','pilot_readiness_decision_id':stable_id('PILOTDEC',req['pilot_request_id'],readiness['readiness_matrix_digest'],length=30),'pilot_request_id':req['pilot_request_id'],'context_id':req['context_id'],'context_version':req['context_version'],'decided_at':decided_at,'state':state,'reason_codes':reasons,'pilot_contract_authored':True,'real_context_evidence_present':req['real_context_evidence_present'],'pilot_ready_non_capital':readiness['pilot_ready_non_capital'],'pilot_execution_allowed':False,'prospective_evidence_claimed':False,'validation_claim_allowed':False,'alpha_claim_allowed':False,'runtime_generation_allowed':False,'runtime_activation_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False,'production_security_ready':False}
    return with_digest(body,'pilot_readiness_decision_digest')

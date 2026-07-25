from __future__ import annotations
from .canonical import stable_id,with_digest
def issue_decision(request:dict,completeness:dict,support:dict,value:dict,uncertainty:dict,decided_at:str)->dict:
    if not completeness['triage_input_complete']: state='INSUFFICIENT_INPUT_FOR_TRIAGE'; pilot_design=False; reasons=['INPUT_COMPLETENESS_FAILED']
    elif support['support_sufficient_for_triage'] and value['value_signal_observed']:
        state='BOUNDED_TRIAGE_COMPLETE_PILOT_DESIGN_ELIGIBLE_NON_CAPITAL'; pilot_design=True; reasons=['TRIAGE_INPUT_COMPLETE','MINIMUM_TRIAGE_SUPPORT_MET','DESCRIPTIVE_VALUE_SIGNAL_OBSERVED','SYNTHETIC_REFERENCE_LIMITATION','VALIDATION_NOT_PERFORMED','PRODUCTION_SECURITY_NOT_READY']
    else:
        state='BOUNDED_TRIAGE_COMPLETE_ESCALATION_REQUIRED'; pilot_design=False; reasons=['TRIAGE_COMPLETE','DESCRIPTIVE_SIGNAL_NOT_ESTABLISHED','VALIDATION_NOT_PERFORMED']
    body={'schema_version':'1.0.0','assessment_result_id':stable_id('TRIAGEDEC',request['assessment_request_id'],state,length=28),'context_id':request['context_id'],'context_version':request['context_version'],'decided_at':decided_at,'decision':state,'reason_codes':reasons,'input_complete':completeness['triage_input_complete'],'triage_support_sufficient':support['support_sufficient_for_triage'],'descriptive_value_signal_observed':value['value_signal_observed'],'first_real_context_pilot_design_allowed':pilot_design,'first_real_context_pilot_execution_allowed':False,'validation_claim_allowed':False,'alpha_claim_allowed':False,'runtime_generation_allowed':False,'runtime_activation_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False,'production_security_ready':False,'claim_ceiling':'RESEARCH_TRIAGE_REFERENCE_ONLY'}
    return with_digest(body,'assessment_result_digest')

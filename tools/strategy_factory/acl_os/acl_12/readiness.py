from __future__ import annotations
from .canonical import stable_id,with_digest
def issue_readiness_decision(bundle:dict,matrix:dict,threats:dict,risk:dict,evidence:dict,decided_at:str)->dict:
    if not matrix['reference_hardening_passed']:
        state='SECURITY_HARDENING_FAILED'; decision='SECURITY_HARDENING_FAILED'; reasons=['ONE_OR_MORE_REFERENCE_CONTROLS_FAILED']
    elif matrix['production_blocker_count']>0:
        state='NON_PRODUCTION_SECURITY_BASELINE'; decision='REFERENCE_SECURITY_HARDENED_PRODUCTION_NOT_READY'; reasons=['REFERENCE_CONTROLS_HARDENED','PRODUCTION_EVIDENCE_INCOMPLETE','UNKNOWN_BLOCKS_PRODUCTION_READINESS','NO_RUNTIME_CANDIDATES','PRODUCTION_KEYS_UNAVAILABLE']
    else:
        state='PRODUCTION_SECURITY_REVIEW_ELIGIBLE_NOT_AUTHORIZED'; decision='PRODUCTION_SECURITY_REVIEW_ELIGIBLE_NOT_AUTHORIZED'; reasons=['SEPARATE_PRODUCTION_SECURITY_AUTHORITY_REQUIRED']
    body={'schema_version':'1.0.0','security_readiness_decision_id':stable_id('SECREADY',bundle['handoff']['runtime_custody_run_id'],matrix['assessment_digest'],length=28),'runtime_custody_run_id':bundle['handoff']['runtime_custody_run_id'],'decided_at':decided_at,'readiness_state':state,'decision':decision,'reason_codes':reasons,'control_matrix_digest':matrix['assessment_digest'],'threat_assessment_digest':threats['assessment_digest'],'risk_register_digest':risk['register_digest'],'evidence_bundle_digest':evidence['evidence_bundle_digest'],'reference_hardening_passed':matrix['reference_hardening_passed'],'production_security_ready':False,'assessment_product_handoff_allowed':True,'runtime_generation_allowed':False,'runtime_activation_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False,'production_key_access_allowed':False}
    return with_digest(body,'readiness_decision_digest')

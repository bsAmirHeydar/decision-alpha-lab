from __future__ import annotations
from .canonical import stable_id,with_digest
def build_generation_manifest(bundle: dict,assessment: dict) -> dict:
    candidates=bundle['runtime']['runtime_candidates']
    body={'schema_version':'1.0.0','source_runtime_candidate_manifest_digest':bundle['runtime']['runtime_candidate_manifest_digest'],'runtime_candidate_count':len(candidates),'generation_count':0,'generations':[],'generation_materialized':False,'runtime_generation_allowed':False,'reason_code':'NO_RUNTIME_CANDIDATES' if not candidates else 'PARITY_AND_AUTHORITY_NOT_SATISFIED'}
    return with_digest(body,'generation_manifest_digest')
def build_signing_plan(generation: dict) -> dict:
    body={'schema_version':'1.0.0','signing_mode':'DETACHED_SIGNATURE_ENVELOPE','key_material_present':False,'signing_key_access_allowed':False,'signature_created':False,'production_verifier_present':False,'revocation_check_required':True,'reason_code':'NO_GENERATION_TO_SIGN' if generation['generation_count']==0 else 'PRODUCTION_KEY_CUSTODY_DEFERRED_TO_ACL12'}
    return with_digest(body,'signing_plan_digest')
def build_conformance_matrix(assessment: dict) -> dict:
    body={'schema_version':'1.0.0','assessment_id':assessment['assessment_id'],'runtime_candidate_count':assessment['runtime_candidate_count'],'vector_set_count':0,'conformance_case_count':0,'cases':[],'mql5_compile_evidence_present':False,'strategy_tester_evidence_present':False,'decision_parity_proven':False,'economics_parity_proven':False,'reason_code':'NO_RUNTIME_CANDIDATES'}
    return with_digest(body,'conformance_matrix_digest')
def issue_decision(bundle: dict,assessment: dict,generation: dict,signing: dict,conformance: dict,decided_at: str) -> dict:
    if bundle['runtime']['runtime_candidate_count']==0:
        state='NO_RUNTIME_CANDIDATES'; decision='NON_EXECUTABLE_NO_RUNTIME_CANDIDATES'; reasons=['NO_RUNTIME_CANDIDATES','RUNTIME_GENERATION_PROHIBITED','SIGNING_NOT_APPLICABLE','ACTIVATION_AUTHORITY_DENIED']
    elif not assessment['all_hard_requirements_satisfied']:
        state='PARITY_INCOMPLETE'; decision='NON_EXECUTABLE_PARITY_INCOMPLETE'; reasons=['RUNTIME_PARITY_REQUIREMENTS_INCOMPLETE','UNKNOWN_BLOCKS_RUNTIME','ACTIVATION_AUTHORITY_DENIED']
    else:
        state='READY_FOR_SIGNED_BUILD_NOT_AUTHORIZED'; decision='ELIGIBLE_FOR_SIGNED_RUNTIME_BUILD_NOT_AUTHORIZED'; reasons=['SEPARATE_BUILD_AND_SIGNING_AUTHORITY_REQUIRED']
    body={'schema_version':'1.0.0','custody_decision_id':stable_id('CUSTDEC',bundle['handoff']['promotion_run_id'],assessment['assessment_digest']),'promotion_run_id':bundle['handoff']['promotion_run_id'],'decided_at':decided_at,'custody_state':state,'decision':decision,'reason_codes':reasons,'runtime_candidate_count':bundle['runtime']['runtime_candidate_count'],'assessment_digest':assessment['assessment_digest'],'generation_manifest_digest':generation['generation_manifest_digest'],'signing_plan_digest':signing['signing_plan_digest'],'conformance_matrix_digest':conformance['conformance_matrix_digest'],'runtime_generation_allowed':False,'signature_creation_allowed':False,'runtime_activation_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False}
    return with_digest(body,'custody_decision_digest')

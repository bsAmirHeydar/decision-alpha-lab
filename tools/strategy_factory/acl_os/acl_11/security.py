from __future__ import annotations
from .canonical import with_digest
def build_tcb() -> dict:
    body={'schema_version':'1.0.0','tcb_mode':'DECLARATION_ONLY','allowed_component_classes':['SIGNED_GENERATION_VERIFIER','COMPATIBILITY_CHECKER','REVOCATION_CHECKER','FAIL_CLOSED_RUNTIME_LOADER','AUDIT_EVENT_WRITER'],'forbidden_component_classes':['TRAINING_ENGINE','ARBITRARY_PLUGIN_LOADER','DYNAMIC_CODE_EXECUTION','NETWORK_DOWNLOADER','SECRET_EXPORTER'],'production_tcb_verified':False,'reason_code':'NO_RUNTIME_GENERATION_AND_PRODUCTION_SECURITY_DEFERRED_TO_ACL12'}
    return with_digest(body,'tcb_digest')
def build_security_report(bundle: dict,decision: dict,tcb: dict) -> dict:
    body={'schema_version':'1.0.0','passed':True,'acl10_integrity_verified':True,'runtime_candidate_count':bundle['runtime']['runtime_candidate_count'],'key_material_present':False,'network_access_allowed':False,'secret_access_allowed':False,'runtime_generation_allowed':False,'runtime_activation_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False,'tcb_digest':tcb['tcb_digest'],'custody_decision_digest':decision['custody_decision_digest'],'forbidden_api_scan_required':True}
    return with_digest(body,'security_report_digest')

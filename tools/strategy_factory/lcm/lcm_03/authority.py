from __future__ import annotations
from .canonical import digest_object
from .errors import AuthorityError

def build_permit(source_handoff_digest: str, classification_id: str, issued_at: str) -> dict:
    permit={'schema_version':'1.0.0','phase_id':'LCM-03','permit_id':'PERMIT_LCM03_REFERENCE_IDENTITY_V1','issuer':'ALPHA_LAB_REFERENCE_ARCHITECTURE_AUTHORITY','issued_at':issued_at,'expires_at':'2099-12-31T23:59:59Z','action':'LCM03_REGISTER_IDENTITY_ALIAS_LOCATOR','classification_id':classification_id,'source_handoff_digest':source_handoff_digest,'reference_only':True,'human_approval_claimed':False,'capabilities':{'register_identity_candidates_allowed':True,'register_legacy_aliases_allowed':True,'build_logical_locators_allowed':True,'enumerate_consumers_allowed':True,'report_collisions_allowed':True,'move_source_files_allowed':False,'delete_source_files_allowed':False,'semantic_refactor_allowed':False,'merge_legacy_implementations_allowed':False,'cutover_allowed':False,'quarantine_source_allowed':False,'runtime_generation_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False,'network_access_allowed':False,'secret_access_allowed':False,'production_key_access_allowed':False}}
    permit['permit_digest']=digest_object(permit,'permit_digest'); return permit

def verify_permit(permit: dict, source_handoff_digest: str):
    if permit.get('action')!='LCM03_REGISTER_IDENTITY_ALIAS_LOCATOR': raise AuthorityError('invalid permit action')
    if permit.get('source_handoff_digest')!=source_handoff_digest: raise AuthorityError('permit source binding mismatch')
    if permit.get('permit_digest')!=digest_object(permit,'permit_digest'): raise AuthorityError('permit digest mismatch')
    denied=['move_source_files_allowed','delete_source_files_allowed','semantic_refactor_allowed','merge_legacy_implementations_allowed','cutover_allowed','quarantine_source_allowed','runtime_generation_allowed','live_order_submission_allowed','capital_activation_allowed','network_access_allowed','secret_access_allowed','production_key_access_allowed']
    if any(permit['capabilities'].get(k) for k in denied): raise AuthorityError('forbidden authority escalation')
    return True

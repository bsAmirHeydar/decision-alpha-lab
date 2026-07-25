from __future__ import annotations
from .canonical import digest_object
from .errors import AuthorityError

def build_permit(source_handoff_digest: str, survey_id: str, issued_at: str) -> dict:
    x={'schema_version':'1.0.0','phase_id':'LCM-02','permit_id':'PERMIT_LCM02_REFERENCE_CLASSIFICATION_V1','issuer':'ALPHA_LAB_REFERENCE_ARCHITECTURE_AUTHORITY','issued_at':issued_at,'expires_at':'2099-12-31T23:59:59Z','action':'LCM02_CLASSIFY_OWNERSHIP_AND_AUTHORITY','survey_id':survey_id,'source_handoff_digest':source_handoff_digest,'reference_only':True,'human_approval_claimed':False,'capabilities':{'classify_artifacts_allowed':True,'propose_owner_roles_allowed':True,'register_authority_boundaries_allowed':True,'move_source_files_allowed':False,'delete_source_files_allowed':False,'semantic_refactor_allowed':False,'merge_legacy_implementations_allowed':False,'cutover_allowed':False,'runtime_generation_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False,'network_access_allowed':False,'secret_access_allowed':False,'production_key_access_allowed':False}}
    x['permit_digest']=digest_object(x,'permit_digest'); return x
def verify_permit(x: dict, source_handoff_digest: str):
    if x.get('action')!='LCM02_CLASSIFY_OWNERSHIP_AND_AUTHORITY': raise AuthorityError('invalid permit action')
    if x.get('source_handoff_digest')!=source_handoff_digest: raise AuthorityError('permit source binding mismatch')
    if x.get('permit_digest')!=digest_object(x,'permit_digest'): raise AuthorityError('permit digest mismatch')
    denied=['move_source_files_allowed','delete_source_files_allowed','semantic_refactor_allowed','merge_legacy_implementations_allowed','cutover_allowed','runtime_generation_allowed','live_order_submission_allowed','capital_activation_allowed','network_access_allowed','secret_access_allowed','production_key_access_allowed']
    if any(x['capabilities'].get(k) for k in denied): raise AuthorityError('forbidden authority escalation')
    return True

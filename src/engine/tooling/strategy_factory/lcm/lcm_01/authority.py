from __future__ import annotations
from .canonical import content_id, digest_object
from .errors import ContractViolation

ACTION='LCM01_RUN_FORENSIC_REPOSITORY_SURVEY'
FORBIDDEN=['MOVE_SOURCE_FILE','DELETE_SOURCE_FILE','SEMANTIC_REFACTOR','MERGE_LEGACY_IMPLEMENTATIONS','CUTOVER_CONSUMER','QUARANTINE_SOURCE','AUTHORIZE_RUNTIME','AUTHORIZE_LIVE_ORDER','ACTIVATE_CAPITAL']

def build_permit(baseline_id: str, baseline_manifest_digest: str, handoff_digest: str, issued_at: str) -> dict:
    material={'phase_id':'LCM-01','action':ACTION,'baseline_id':baseline_id,'baseline_manifest_digest':baseline_manifest_digest,'source_handoff_digest':handoff_digest,'issued_at':issued_at}
    permit={
      'schema_version':'1.0.0','permit_id':content_id('LCM01PERMIT',material),
      **material,'issuer':'LCM_PROGRAM_REFERENCE_AUTHORITY','expires_at':'2027-07-18T00:00:00Z',
      'human_approval_status':'PENDING_NON_DESTRUCTIVE_SURVEY_ALLOWED',
      'network_access_allowed':False,'secret_access_allowed':False,'source_move_allowed':False,
      'source_delete_allowed':False,'semantic_refactor_allowed':False,'runtime_authority_allowed':False,
      'live_order_submission_allowed':False,'capital_activation_allowed':False,
      'forbidden_actions':FORBIDDEN,'permit_digest':''}
    permit['permit_digest']=digest_object(permit,'permit_digest')
    return permit

def verify_permit(value: dict, baseline_id: str, manifest_digest: str, handoff_digest: str) -> None:
    if value.get('permit_digest')!=digest_object(value,'permit_digest'): raise ContractViolation('permit digest mismatch')
    expected={'phase_id':'LCM-01','action':ACTION,'baseline_id':baseline_id,'baseline_manifest_digest':manifest_digest,'source_handoff_digest':handoff_digest}
    for k,v in expected.items():
        if value.get(k)!=v: raise ContractViolation(f'permit binding mismatch: {k}')
    for k in ['network_access_allowed','secret_access_allowed','source_move_allowed','source_delete_allowed','semantic_refactor_allowed','runtime_authority_allowed','live_order_submission_allowed','capital_activation_allowed']:
        if value.get(k) is not False: raise ContractViolation(f'authority escalation forbidden: {k}')

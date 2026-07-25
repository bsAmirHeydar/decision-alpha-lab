from __future__ import annotations
from .canonical import with_digest
def build_incident_readiness()->dict:
    playbooks=['KEY_COMPROMISE','ARTIFACT_TAMPERING','DEPENDENCY_COMPROMISE','AUDIT_LEDGER_TAMPER','UNAUTHORIZED_ACTIVATION_ATTEMPT','CAPITAL_BOUNDARY_BREACH']
    return with_digest({'schema_version':'1.0.0','readiness_id':'ACL12_INCIDENT_RESPONSE_READINESS_V1','playbooks':playbooks,'playbook_count':len(playbooks),'severity_model_defined':True,'evidence_preservation_defined':True,'communication_matrix_defined':True,'tabletop_exercise_completed':False,'production_on_call_verified':False,'reason_codes':['REFERENCE_PLAYBOOKS_DEFINED','TABLETOP_EVIDENCE_MISSING','PRODUCTION_ON_CALL_EVIDENCE_MISSING']},'readiness_digest')
def build_revocation_plan()->dict:
    return with_digest({'schema_version':'1.0.0','plan_id':'ACL12_REVOCATION_QUARANTINE_PLAN_V1','quarantine_triggers':['DIGEST_MISMATCH','SIGNATURE_FAILURE','DEPENDENCY_RECALL','KEY_COMPROMISE','UNAUTHORIZED_AUTHORITY_ESCALATION','AUDIT_CHAIN_BREAK'],'actions':['DENY_LOAD','QUARANTINE_ARTIFACT','REVOKE_GENERATION','PRESERVE_EVIDENCE','NOTIFY_INCIDENT_COMMANDER'],'automatic_live_activation_allowed':False,'rollback_generation_required':True,'production_drill_completed':False},'plan_digest')

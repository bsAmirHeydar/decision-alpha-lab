from __future__ import annotations
from .canonical import with_digest
ROLES=['SECURITY_ASSESSOR','RELEASE_SIGNER','RUNTIME_ACTIVATOR','CAPITAL_OWNER','INCIDENT_COMMANDER','AUDIT_REVIEWER']
def build_operator_separation()->dict:
    conflicts=[['SECURITY_ASSESSOR','RELEASE_SIGNER'],['RELEASE_SIGNER','RUNTIME_ACTIVATOR'],['RUNTIME_ACTIVATOR','CAPITAL_OWNER'],['INCIDENT_COMMANDER','AUDIT_REVIEWER']]
    return with_digest({'schema_version':'1.0.0','matrix_id':'ACL12_OPERATOR_SEPARATION_V1','roles':ROLES,'conflicts':[{'role_a':a,'role_b':b,'same_principal_allowed':False} for a,b in conflicts],'minimum_independent_approvers':2,'self_approval_allowed':False,'reference_policy_defined':True,'production_identity_provider_verified':False},'matrix_digest')

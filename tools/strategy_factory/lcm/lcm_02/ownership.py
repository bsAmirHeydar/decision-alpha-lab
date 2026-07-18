from __future__ import annotations
from .canonical import digest_object

def normalize(value: str) -> str:
    return ''.join(c if c.isalnum() else '_' for c in value.upper()).strip('_')
def family_roles(families: list[str]) -> dict:
    base=[
      {'role_id':'PROGRAM_OWNER','role_type':'PROGRAM_OWNER','assignee_id':None,'assignment_status':'UNRESOLVED_HUMAN_ASSIGNEE','human_approval_required':True},
      {'role_id':'MIGRATION_ENGINEER','role_type':'MIGRATION_ENGINEER','assignee_id':'ALPHA_LAB_REFERENCE_AUTOMATION','assignment_status':'REFERENCE_AUTOMATION_ASSIGNED','human_approval_required':False},
      {'role_id':'INDEPENDENT_PARITY_REVIEWER','role_type':'INDEPENDENT_REVIEWER','assignee_id':None,'assignment_status':'UNRESOLVED_HUMAN_ASSIGNEE','human_approval_required':True},
      {'role_id':'SECURITY_REVIEWER','role_type':'SECURITY_REVIEWER','assignee_id':None,'assignment_status':'UNRESOLVED_HUMAN_ASSIGNEE','human_approval_required':True},
      {'role_id':'KNOWLEDGE_CURATOR','role_type':'DOCUMENTATION_OWNER','assignee_id':None,'assignment_status':'UNRESOLVED_HUMAN_ASSIGNEE','human_approval_required':True},
      {'role_id':'REPOSITORY_STEWARD','role_type':'CODE_OWNER','assignee_id':None,'assignment_status':'UNRESOLVED_HUMAN_ASSIGNEE','human_approval_required':True},
      {'role_id':'RELEASE_OPERATOR','role_type':'RELEASE_OWNER','assignee_id':None,'assignment_status':'UNRESOLVED_HUMAN_ASSIGNEE','human_approval_required':True},
    ]
    for fam in sorted(families):
        base.append({'role_id':'DOMAIN_OWNER_'+normalize(fam),'role_type':'SEMANTIC_OWNER','family':fam,'assignee_id':None,'assignment_status':'UNRESOLVED_HUMAN_ASSIGNEE','human_approval_required':True})
        base.append({'role_id':'CODE_OWNER_'+normalize(fam),'role_type':'CODE_OWNER','family':fam,'assignee_id':None,'assignment_status':'UNRESOLVED_HUMAN_ASSIGNEE','human_approval_required':True})
    reg={'schema_version':'1.0.0','registry_id':'LCM02_OWNER_ROLE_REGISTRY_V1','assignment_policy':'ROLE_BINDING_IS_NOT_HUMAN_APPROVAL; UNKNOWN_IS_BLOCKING; COMMIT_AUTHORSHIP_IS_NOT_OWNERSHIP','human_approval_claimed':False,'roles':base}
    reg['registry_digest']=digest_object(reg,'registry_digest'); return reg
def owner_binding(family: str, role: str, security_sensitive: bool):
    f=normalize(family)
    semantic='DOMAIN_OWNER_'+f
    code='CODE_OWNER_'+f
    documentation='KNOWLEDGE_CURATOR'
    security='SECURITY_REVIEWER' if security_sensitive else None
    blocking=['SEMANTIC_OWNER_ASSIGNEE_PENDING','CODE_OWNER_ASSIGNEE_PENDING']
    if role in {'DOCUMENTATION','GENERATED_PROJECTION','SOURCE_EVIDENCE'}: blocking.append('DOCUMENTATION_OWNER_ASSIGNEE_PENDING')
    if security_sensitive: blocking.append('SECURITY_REVIEWER_ASSIGNEE_PENDING')
    return {'semantic_owner_role':semantic,'code_owner_role':code,'documentation_owner_role':documentation,'security_reviewer_role':security,'owner_resolution_status':'ROLE_BOUND_HUMAN_ASSIGNEE_PENDING','owner_evidence':['SURVEY_FAMILY_CANDIDATE','LCM02_ROLE_MAPPING_POLICY'],'ownership_is_human_approved':False,'ownership_blockers':sorted(set(blocking))}

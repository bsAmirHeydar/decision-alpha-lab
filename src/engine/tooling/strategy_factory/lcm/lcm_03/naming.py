from __future__ import annotations
from pathlib import PurePosixPath
from .canonical import normalize_token
from .registries import IDENTITY_KINDS,ROLE_TO_KIND

def semantic_stem(path: str) -> str:
    stem=PurePosixPath(path).stem
    for prefix in ('EXP_','TEST_','TST_','DIAG_'):
        if stem.upper().startswith(prefix): stem=stem[len(prefix):]
    return normalize_token(stem,40)
def propose_identity(record: dict) -> dict|None:
    role=record['artifact_role']
    kind=ROLE_TO_KIND.get(role)
    if not kind: return None
    prefix,_=IDENTITY_KINDS[kind]
    family=normalize_token(record['family_candidate'],32)
    stem=semantic_stem(record['artifact_path'])
    discriminator=record['classification_id'].split('_')[-1][:8]
    identity_id=f'{prefix}_{family}_{stem}_{discriminator}_V1'
    status='PROVISIONAL_UNMERGED_IDENTITY_CANDIDATE'
    if record.get('protected_platform_asset'): status='PROTECTED_PLATFORM_TECHNICAL_IDENTITY'
    if record.get('security_sensitive'): status='SECURITY_REVIEW_BLOCKED'
    return {'identity_id':identity_id,'identity_kind':kind,'identity_prefix':prefix,'semantic_name_candidate':stem,'family_candidate':record['family_candidate'],'major_version':1,'semantic_version':'1.0.0','identity_status':status,'source_classification_id':record['classification_id'],'source_artifact_path':record['artifact_path'],'source_artifact_sha256':record['artifact_sha256'],'source_role':role,'source_activity_status':record['activity_status'],'protected_platform_asset':record['protected_platform_asset'],'security_sensitive':record['security_sensitive'],'owner_resolution_status':record['owner_resolution_status'],'semantic_owner_role':record['semantic_owner_role'],'code_owner_role':record['code_owner_role'],'human_semantic_approval_claimed':False,'merge_claimed':False,'path_independent_after_registration':True,'identity_digest':None}

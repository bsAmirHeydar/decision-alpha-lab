from pathlib import PurePosixPath
from .canonical import content_id,digest_object,slug
from .path_policy import validate
from .registries import PACKAGE_ROOTS
from .layering import layer_for
def ext_name(path):
    p=PurePosixPath(path);stem=''.join(c if (c.isalnum() or c in '._-') else '_' for c in p.stem).rstrip(' .')[:56] or 'artifact';suffix=''.join(c if (c.isalnum() or c=='.') else '_' for c in p.suffix)[:12];return (stem+suffix).rstrip(' .')
def identity_root(identity):
    if identity.get('protected_platform_asset'):return identity['source_artifact_path']
    base=PACKAGE_ROOTS.get(identity['identity_kind'],'registry/history/lcm/support_artifacts');iid=identity['identity_id'];segment=iid if len(iid)<=72 else iid[:56]+'__'+identity['identity_digest'].split(':')[-1][:12].upper();return f"{base}/{segment}"
def materialization_status(rec):
    if rec.get('protected_platform_asset'):return 'RETAINED_IN_PLACE'
    if rec.get('security_sensitive'):return 'BLOCKED_SECURITY_REVIEW'
    if rec.get('owner_resolution_status')!='HUMAN_APPROVED':return 'BLOCKED_OWNER_APPROVAL'
    if rec.get('primary_disposition')=='MERGE_AFTER_EQUIVALENCE_PROOF':return 'BLOCKED_EQUIVALENCE_REVIEW'
    if rec.get('primary_disposition') in ('REWRITE_WITH_PARITY','EXTRACT_SHARED_LOGIC','WRAP_LEGACY'):return 'BLOCKED_PARITY'
    return 'NOT_MATERIALIZED'
def map_identity(identity):
    target=identity_root(identity);validate(target)
    obj={"schema_version":"1.0.0","identity_id":identity['identity_id'],"identity_kind":identity['identity_kind'],"source_artifact_path":identity['source_artifact_path'],"source_artifact_sha256":identity['source_artifact_sha256'],"target_package_root":target,"target_layer":layer_for(identity['source_role'],identity['source_artifact_path']),"canonical_path_materialized":False,"owner_resolution_status":identity['owner_resolution_status'],"identity_status":identity['identity_status'],"protected_platform_asset":identity['protected_platform_asset'],"security_sensitive":identity['security_sensitive'],"materialization_status":'RETAINED_IN_PLACE' if identity['protected_platform_asset'] else ('BLOCKED_SECURITY_REVIEW' if identity['security_sensitive'] else 'BLOCKED_OWNER_APPROVAL'),"mapping_digest":None};obj['mapping_digest']=digest_object(obj,'mapping_digest');return obj
def _role_base(rec):return PACKAGE_ROOTS.get(rec['artifact_role'],'tests/legacy/strategy_factory/migration/quarantine/unknown_role')
def map_artifact(rec,identity_by_path):
    path=rec['artifact_path'];sha=rec['artifact_sha256'].split(':')[-1];family=slug(rec['family_candidate'],40);name=ext_name(path);unique=rec['classification_id'].split('_')[-1][:10];disp=rec['primary_disposition'];identity=identity_by_path.get(path)
    if rec['protected_platform_asset'] or disp=='KEEP_CANONICAL':outcome='RETAIN_CURRENT';target=path
    elif disp=='ARCHIVE_REFERENCE_ONLY':outcome='PROPOSE_ARCHIVE';target=f"registry/archives/legacy/{family}/{sha[:16]}/{unique}_{name}"
    elif disp=='QUARANTINE_UNCERTAIN':outcome='PROPOSE_QUARANTINE';target=f"tests/legacy/strategy_factory/migration/quarantine/uncertain/{family}/{sha[:16]}/{unique}_{name}"
    elif disp=='SECURITY_RESTRICTED':outcome='PROPOSE_SECURITY_RESTRICTED';target=f"registry/security_restricted/legacy/{family}/{sha[:16]}/{unique}_{name}"
    elif disp=='MERGE_AFTER_EQUIVALENCE_PROOF':outcome='BLOCKED_EQUIVALENCE_REVIEW';target=f"tests/legacy/strategy_factory/migration/quarantine/equivalence_pending/{family}/{sha[:16]}/{unique}_{name}"
    elif rec['artifact_role']=='GENERATED_PROJECTION':outcome='PROPOSE_GENERATED_PROJECTION';target=f"registry/generated_projections/{family}/{sha[:16]}/{unique}_{name}"
    elif disp=='WRAP_LEGACY':
        outcome='PROPOSE_COMPATIBILITY_WRAPPER';target=(f"mql5/Include/AlphaLab/ContextOS/Compatibility/{family}/{sha[:12]}_{unique}_{name}" if path.lower().endswith(('.mq5','.mqh')) else f"lab/11_strategy_factory/adapters/compatibility/{family}/{sha[:12]}_{unique}_{name}")
    else:
        outcome='PROPOSE_CANONICAL_PACKAGE';base=identity_root(identity) if identity else _role_base(rec)
        if base=='__RETAIN_CURRENT__':target=path;outcome='RETAIN_CURRENT'
        else:target=f"{base}/migration/source_evidence/{sha[:12]}_{unique}_{name}"
    validate(target)
    obj={"schema_version":"1.0.0","target_mapping_id":content_id('TARGETMAP',[path,rec['artifact_sha256'],target]),"artifact_path":path,"artifact_sha256":rec['artifact_sha256'],"classification_id":rec['classification_id'],"family_candidate":rec['family_candidate'],"artifact_role":rec['artifact_role'],"activity_status":rec['activity_status'],"primary_disposition":disp,"identity_id":identity['identity_id'] if identity else None,"target_outcome":outcome,"target_path":target,"target_layer":layer_for(rec['artifact_role'],path),"materialization_status":materialization_status(rec),"source_move_authorized":False,"source_delete_authorized":False,"semantic_refactor_authorized":False,"cutover_authorized":False,"runtime_authorized":False,"live_order_authorized":False,"capital_authorized":False,"mapping_digest":None};obj['mapping_digest']=digest_object(obj,'mapping_digest');return obj

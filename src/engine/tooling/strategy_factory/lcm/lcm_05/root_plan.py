from pathlib import PurePosixPath
from .canonical import content_id,digest_object
from .path_policy import validate
def map_root(row):
    path=row['path'];cls=row['classification'];sha=row['sha256'].split(':')[-1];raw=PurePosixPath(path).name;name=''.join(c if (c.isalnum() or c in '._-') else '_' for c in raw).rstrip(' .')[:90] or 'artifact'
    if cls=='ROOT_CANONICAL':outcome='RETAIN_CURRENT';target=path
    elif 'INSTALL' in cls:outcome='PROPOSE_RELOCATION';target=f"tools/release/powershell/legacy/{sha[:12]}_{name}"
    elif 'COMMIT' in cls:outcome='PROPOSE_RELOCATION';target=f"registry/history/releases/commit_records/{sha[:12]}_{name}"
    elif 'BINARY' in cls or name.lower().endswith(('.zip','.7z','.rar')):outcome='PROPOSE_ARCHIVE';target=f"registry/archives/patches/{sha[:16]}/{name}"
    elif 'RELEASE' in cls or 'MANIFEST' in name.upper() or 'QA_REPORT' in name.upper() or 'FILE_HASH' in name.upper() or 'FILE_INDEX' in name.upper():outcome='PROPOSE_RELOCATION';target=f"registry/history/releases/legacy_root/{sha[:16]}/{name}"
    elif row.get('review_required','').lower()=='true':outcome='PROPOSE_QUARANTINE';target=f"tests/legacy/strategy_factory/migration/quarantine/root_review/{sha[:16]}/{name}"
    else:outcome='PROPOSE_RELOCATION';target=f"registry/history/releases/program_artifacts/{sha[:16]}/{name}"
    validate(target)
    obj={"schema_version":"1.0.0","root_plan_id":content_id('ROOTPLAN',[path,target]),"source_path":path,"source_sha256":row['sha256'],"source_classification":cls,"target_outcome":outcome,"target_path":target,"move_performed":False,"delete_performed":False,"review_required":row.get('review_required','').lower()=='true',"plan_digest":None};obj['plan_digest']=digest_object(obj,'plan_digest');return obj

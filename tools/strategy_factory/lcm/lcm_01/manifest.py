from __future__ import annotations
from pathlib import Path
from .canonical import digest_object, sha256_file

def build_output_manifest(root: Path, survey_id: str) -> dict:
    artifacts=[]
    for p in sorted(root.rglob('*')):
        if not p.is_file() or p.name=='output_manifest.json': continue
        artifacts.append({'path':p.relative_to(root).as_posix(),'size_bytes':p.stat().st_size,'sha256':sha256_file(p)})
    v={'schema_version':'1.0.0','phase_id':'LCM-01','survey_id':survey_id,'artifact_count':len(artifacts),'artifacts':artifacts,'source_move_performed':False,'source_delete_performed':False,'output_manifest_digest':''}
    v['output_manifest_digest']=digest_object(v,'output_manifest_digest'); return v

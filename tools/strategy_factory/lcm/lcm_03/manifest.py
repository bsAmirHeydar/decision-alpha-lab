from __future__ import annotations
from pathlib import Path
from .canonical import digest_object,sha256_file

def build(root: Path, identity_run_id: str):
    artifacts=[]
    for p in sorted(root.rglob('*')):
        if p.is_file() and p.name!='output_manifest.json':
            artifacts.append({'path':p.relative_to(root).as_posix(),'size_bytes':p.stat().st_size,'sha256':sha256_file(p)})
    out={'schema_version':'1.0.0','phase_id':'LCM-03','identity_run_id':identity_run_id,'artifact_count':len(artifacts),'artifacts':artifacts,'output_manifest_digest':None};out['output_manifest_digest']=digest_object(out,'output_manifest_digest');return out

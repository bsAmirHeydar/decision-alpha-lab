from __future__ import annotations
from pathlib import Path
from .canonical import digest_object,sha256_file

def build(root: Path, classification_id: str):
    items=[]
    for p in sorted(root.rglob('*')):
        if p.is_file() and p.name!='output_manifest.json':
            rel=p.relative_to(root).as_posix(); items.append({'path':rel,'size_bytes':p.stat().st_size,'sha256':sha256_file(p)})
    x={'schema_version':'1.0.0','phase_id':'LCM-02','classification_id':classification_id,'artifact_count':len(items),'artifacts':items,'source_move_performed':False,'source_delete_performed':False,'semantic_refactor_performed':False}
    x['output_manifest_digest']=digest_object(x,'output_manifest_digest'); return x

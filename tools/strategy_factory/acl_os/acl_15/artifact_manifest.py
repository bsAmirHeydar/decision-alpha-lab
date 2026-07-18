from __future__ import annotations
from pathlib import Path
from .canonical import digest_file,with_digest
from .io import safe_rel
def build_output_manifest(root:Path,run_id:str)->dict:
    files=[]
    for p in sorted(x for x in root.rglob('*') if x.is_file() and not x.is_symlink()):
        rel=p.relative_to(root).as_posix()
        if rel in {'output_manifest.json','fleet_closure_receipt.json'}: continue
        files.append({'path':rel,'size_bytes':p.stat().st_size,'digest':digest_file(p)})
    return with_digest({'schema_version':'1.0.0','fleet_closure_run_id':run_id,'artifact_count':len(files),'files':files,'self_reference_policy':'MANIFEST_AND_RECEIPT_EXCLUDED_AND_MUTUALLY_BOUND'},'manifest_digest')
def verify_output_manifest(root:Path,doc:dict)->bool:
    from .canonical import verify_embedded_digest
    if not verify_embedded_digest(doc,'manifest_digest'): return False
    rows=doc.get('files')
    if not isinstance(rows,list) or doc.get('artifact_count')!=len(rows): return False
    seen=set()
    for row in rows:
        try: rel=safe_rel(row['path'])
        except Exception: return False
        if rel in seen: return False
        seen.add(rel); p=root/rel
        if not p.is_file() or p.is_symlink() or p.stat().st_size!=row.get('size_bytes') or digest_file(p)!=row.get('digest'): return False
    return True

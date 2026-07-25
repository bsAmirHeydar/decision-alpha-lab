from __future__ import annotations
from pathlib import Path
from .canonical import digest_file,digest_object
def build_output_manifest(root:Path,run_id:str)->dict:
    excluded={'output_manifest.json','first_real_context_pilot_receipt.json'}; files=[]
    for p in sorted(x for x in root.rglob('*') if x.is_file() and x.name not in excluded):
        files.append({'path':p.relative_to(root).as_posix(),'size_bytes':p.stat().st_size,'digest':digest_file(p)})
    body={'schema_version':'1.0.0','pilot_run_id':run_id,'artifact_count':len(files),'files':files,'self_reference_policy':'MANIFEST_AND_RECEIPT_EXCLUDED_AND_MUTUALLY_BOUND'}
    return {**body,'manifest_digest':digest_object(body)}
def verify_output_manifest(root:Path,m:dict)->bool:
    if m.get('manifest_digest')!=digest_object({k:v for k,v in m.items() if k!='manifest_digest'}): return False
    if m.get('artifact_count')!=len(m.get('files',[])): return False
    seen=set()
    for item in m.get('files',[]):
        rel=item.get('path','')
        if rel in seen or rel.startswith('/') or '..' in rel.split('/'): return False
        seen.add(rel); p=root/rel
        if not p.is_file() or p.is_symlink() or p.stat().st_size!=item.get('size_bytes') or digest_file(p)!=item.get('digest'): return False
    return True

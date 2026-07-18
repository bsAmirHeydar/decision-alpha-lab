from __future__ import annotations
from pathlib import Path
from .canonical import digest_file,digest_object
def build_output_manifest(root:Path,memory_run_id:str)->dict:
    excluded={'output_manifest.json','memory_receipt.json'}; files=[]
    for p in sorted(x for x in root.rglob('*') if x.is_file() and x.name not in excluded):
        files.append({'path':p.relative_to(root).as_posix(),'size_bytes':p.stat().st_size,'digest':digest_file(p)})
    body={'schema_version':'1.0.0','memory_run_id':memory_run_id,'artifact_count':len(files),'files':files,'self_reference_policy':'MANIFEST_AND_RECEIPT_EXCLUDED_AND_MUTUALLY_BOUND'}
    return {**body,'manifest_digest':digest_object(body)}
def verify_output_manifest(root:Path,manifest:dict)->bool:
    if manifest.get('manifest_digest')!=digest_object({k:v for k,v in manifest.items() if k!='manifest_digest'}): return False
    if len(manifest.get('files',[]))!=manifest.get('artifact_count'): return False
    seen=set()
    for item in manifest.get('files',[]):
        if item['path'] in seen: return False
        seen.add(item['path']); p=root/item['path']
        if not p.is_file() or p.is_symlink() or p.stat().st_size!=item['size_bytes'] or digest_file(p)!=item['digest']: return False
    return True

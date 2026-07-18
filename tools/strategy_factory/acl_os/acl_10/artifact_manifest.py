from __future__ import annotations
from pathlib import Path
from .canonical import digest_file, digest_object
def build_output_manifest(root: Path, promotion_run_id: str) -> dict:
    excluded = {'output_manifest.json','promotion_receipt.json'}
    files = []
    for path in sorted(x for x in root.rglob('*') if x.is_file() and x.name not in excluded):
        files.append({'path':path.relative_to(root).as_posix(),'size_bytes':path.stat().st_size,'digest':digest_file(path)})
    body = {'schema_version':'1.0.0','promotion_run_id':promotion_run_id,'artifact_count':len(files),'files':files,'self_reference_policy':'MANIFEST_AND_RECEIPT_EXCLUDED_AND_MUTUALLY_BOUND'}
    return {**body,'manifest_digest':digest_object(body)}
def verify_output_manifest(root: Path, manifest: dict) -> bool:
    if manifest.get('manifest_digest') != digest_object({k:v for k,v in manifest.items() if k != 'manifest_digest'}): return False
    if len(manifest.get('files',[])) != manifest.get('artifact_count'): return False
    seen = set()
    for item in manifest.get('files',[]):
        if item['path'] in seen: return False
        seen.add(item['path'])
        path = root/item['path']
        if not path.is_file() or path.is_symlink() or path.stat().st_size != item['size_bytes'] or digest_file(path) != item['digest']: return False
    return True

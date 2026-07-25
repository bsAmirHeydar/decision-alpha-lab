from __future__ import annotations
from pathlib import Path
from .canonical import digest_file, digest_object

def build_output_manifest(root: Path,batch_id: str) -> dict:
    excluded={"output_manifest.json","batch_receipt.json"}
    files=[]
    for path in sorted(p for p in root.rglob("*") if p.is_file() and p.name not in excluded):
        rel=path.relative_to(root).as_posix()
        files.append({"path":rel,"size_bytes":path.stat().st_size,"digest":digest_file(path)})
    body={"schema_version":"1.0.0","batch_id":batch_id,"artifact_count":len(files),"files":files,"self_reference_policy":"MANIFEST_AND_RECEIPT_EXCLUDED_AND_MUTUALLY_BOUND"}
    return {**body,"manifest_digest":digest_object(body)}

def verify_output_manifest(root: Path,manifest: dict) -> bool:
    if manifest.get("manifest_digest")!=digest_object({k:v for k,v in manifest.items() if k!="manifest_digest"}):
        return False
    for item in manifest.get("files",[]):
        p=root/item["path"]
        if not p.is_file() or p.is_symlink() or p.stat().st_size!=item["size_bytes"] or digest_file(p)!=item["digest"]:
            return False
    return len(manifest.get("files",[]))==manifest.get("artifact_count")

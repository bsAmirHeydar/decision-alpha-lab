from __future__ import annotations
from pathlib import Path
from .canonical import digest_object,file_digest

def build_manifest(root:Path)->dict:
    files=[]
    for p in sorted(x for x in root.rglob("*") if x.is_file() and x.name not in {"output_manifest.json","setup_migration_receipt.json"}):
        files.append({"path":p.relative_to(root).as_posix(),"size_bytes":p.stat().st_size,"sha256":file_digest(p)})
    body={"schema_version":"1.0.0","file_count":len(files),"files":files}
    return {**body,"manifest_digest":digest_object(body)}

from __future__ import annotations
from pathlib import Path
from .canonical import file_digest,digest_object
from .constants import MIGRATION_ID
def build_manifest(root:Path)->dict:
    rows=[]
    for p in sorted(x for x in root.rglob("*") if x.is_file() and x.name not in {"output_manifest.json","treatment_boundary_receipt.json"}):rows.append({"path":p.relative_to(root).as_posix(),"sha256":file_digest(p),"size_bytes":p.stat().st_size})
    body={"schema_version":"1.0.0","migration_id":MIGRATION_ID,"file_count":len(rows),"total_size_bytes":sum(x["size_bytes"] for x in rows),"files":rows};return {**body,"manifest_digest":digest_object(body)}

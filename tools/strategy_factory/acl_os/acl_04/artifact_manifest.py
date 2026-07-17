from __future__ import annotations
from pathlib import Path
from .canonical import digest_file, digest_object


def build_manifest(output_root: Path, context_id: str, context_version: str) -> dict:
    files=[]
    for path in sorted(p for p in output_root.rglob("*") if p.is_file() and p.name not in {"output_manifest.json","factory_receipt.json"}):
        files.append({"path":path.relative_to(output_root).as_posix(),"digest":digest_file(path),"size_bytes":path.stat().st_size})
    body={"schema_version":"1.0.0","context_id":context_id,"context_version":context_version,"artifact_count":len(files),"files":files}
    return {**body,"manifest_digest":digest_object(body)}

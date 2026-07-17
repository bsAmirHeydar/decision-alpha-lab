from __future__ import annotations
from pathlib import Path
from typing import Any
from .canonical import digest_file,digest_object

def build_output_manifest(output_root:Path,context_id:str,context_version:str,source_digest:str)->dict[str,Any]:
    entries=[]
    for p in sorted(output_root.rglob("*")):
        if p.is_file() and p.name!="output_manifest.json":
            entries.append({"relative_path":p.relative_to(output_root).as_posix(),"bytes":p.stat().st_size,"content_digest":digest_file(p)})
    body={"schema_version":"1.0.0","context_id":context_id,"context_version":context_version,"source_digest":source_digest,"entries":entries,"entry_count":len(entries)}
    return {**body,"manifest_digest":digest_object(body)}

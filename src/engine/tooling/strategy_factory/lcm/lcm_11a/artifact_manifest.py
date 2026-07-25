from __future__ import annotations
from pathlib import Path
from .canonical import digest_object, file_digest

def build_output_manifest(root: Path, metadata: dict) -> dict:
    files=[]
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.name!="output_manifest.json":
            files.append({"path":path.relative_to(root).as_posix(),"sha256":file_digest(path),"size_bytes":path.stat().st_size})
    value={**metadata,"files":files,"file_count":len(files),"total_size_bytes":sum(x["size_bytes"] for x in files)}
    value["output_manifest_digest"]=digest_object(value,"output_manifest_digest"); return value

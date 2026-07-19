from __future__ import annotations
from pathlib import Path
from .canonical import digest_object, file_digest
from .io import write_json


def build(package_root: Path) -> dict:
    files=[]
    for path in sorted(p for p in package_root.rglob('*') if p.is_file() and p.name != 'output_manifest.json'):
        files.append({"path":path.relative_to(package_root).as_posix(),"size_bytes":path.stat().st_size,"sha256":file_digest(path)})
    obj={"schema_version":"1.0.0","manifest_type":"LCM08A_CONTEXT_PORTFOLIO_PACKAGE","file_count":len(files),"files":files,"manifest_digest":None}
    obj["manifest_digest"]=digest_object(obj,"manifest_digest")
    write_json(package_root/'output_manifest.json',obj)
    return obj

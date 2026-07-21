from __future__ import annotations
from pathlib import Path
from .canonical import digest_object, file_digest

def build_manifest(root: Path, excluded_names: set[str] | None = None) -> dict:
    excluded=excluded_names or {'output_manifest.json','treatment_inventory_receipt.json'}
    files=[]
    for path in sorted(p for p in root.rglob('*') if p.is_file() and p.name not in excluded):
        files.append({"path":path.relative_to(root).as_posix(),"size_bytes":path.stat().st_size,"sha256":file_digest(path)})
    body={"schema_version":"1.0.0","file_count":len(files),"total_size_bytes":sum(x['size_bytes'] for x in files),"files":files}
    return {**body,"manifest_digest":digest_object(body)}

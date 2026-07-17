from __future__ import annotations
from pathlib import Path
from typing import Any
from .canonical import digest_file,digest_object
from .io import ensure_contained

IGNORED_DIRS={"generated","reports","intake","__pycache__",".pytest_cache"}

def build_source_snapshot(context_root:Path, package:dict[str,Any], compiler_version:str)->dict[str,Any]:
    root=context_root.resolve(); files=[]
    for path in sorted(root.rglob("*")):
        if path.is_symlink(): raise ValueError(f"symlink is forbidden in Context source: {path}")
        if not path.is_file(): continue
        rel=path.relative_to(root).as_posix()
        if any(part in IGNORED_DIRS for part in path.relative_to(root).parts): continue
        ensure_contained(root,path)
        files.append({"path":rel,"bytes":path.stat().st_size,"digest":digest_file(path)})
    body={"schema_version":"1.0.0","context_id":package["manifest"]["context_id"],"context_version":package["manifest"]["context_version"],"compiler_version":compiler_version,"files":files,"source_package_digest":digest_object({k:v for k,v in package.items() if not k.startswith("_")})}
    return {**body,"snapshot_digest":digest_object(body)}

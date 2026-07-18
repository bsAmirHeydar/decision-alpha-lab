from __future__ import annotations
import json,os
from pathlib import Path
from typing import Any
from .errors import ContractError,PublicationError
def load_json(path:Path)->dict[str,Any]:
    try: value=json.loads(path.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc: raise ContractError(f"ACL12_JSON_LOAD_FAILED:{path}:{exc}") from exc
    if not isinstance(value,dict): raise ContractError(f"ACL12_TOP_LEVEL_OBJECT_REQUIRED:{path}")
    return value
def dump_json(path:Path,value:Any)->None:
    path.parent.mkdir(parents=True,exist_ok=True); tmp=path.with_name(path.name+".tmp")
    tmp.write_text(json.dumps(value,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8",newline="\n"); os.replace(tmp,path)
def safe_relative(root:Path,relative:str)->Path:
    if not relative or Path(relative).is_absolute(): raise ContractError("ACL12_ABSOLUTE_OR_EMPTY_PATH_DENIED")
    target=(root/relative).resolve()
    try: target.relative_to(root.resolve())
    except ValueError as exc: raise ContractError("ACL12_PATH_ESCAPE_DENIED") from exc
    if target.is_symlink(): raise ContractError("ACL12_SYMLINK_DENIED")
    return target
def atomic_publish(staging:Path,destination:Path)->None:
    if destination.exists() and any(destination.iterdir()): raise PublicationError("ACL12_DESTINATION_NON_EMPTY")
    if destination.exists(): destination.rmdir()
    destination.parent.mkdir(parents=True,exist_ok=True); os.replace(staging,destination)

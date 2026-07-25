from __future__ import annotations
import json, os
from pathlib import Path
from typing import Any
from .canonical import canonical_bytes
from .errors import ContractError, PublicationError

def load_json(path: Path) -> dict[str, Any]:
    try:
        value=json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"cannot load JSON {path}: {exc}") from exc
    if not isinstance(value,dict):
        raise ContractError(f"top-level object required: {path}")
    return value

def dump_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    payload=json.dumps(value,indent=2,sort_keys=True,ensure_ascii=False)+"\n"
    tmp=path.with_name(path.name+".tmp")
    tmp.write_text(payload,encoding="utf-8",newline="\n")
    os.replace(tmp,path)

def dump_canonical(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_name(path.name+".tmp")
    tmp.write_bytes(canonical_bytes(value)+b"\n")
    os.replace(tmp,path)

def safe_relative(root: Path, relative: str) -> Path:
    if not relative or Path(relative).is_absolute():
        raise ContractError("absolute or empty path denied")
    target=(root/relative).resolve(); resolved=root.resolve()
    try:
        target.relative_to(resolved)
    except ValueError as exc:
        raise ContractError(f"path escapes root: {relative}") from exc
    return target

def require_clean_output(path: Path) -> None:
    if path.exists() and any(path.iterdir()):
        raise PublicationError(f"output root must be empty: {path}")
    path.mkdir(parents=True,exist_ok=True)

def atomic_publish(staging: Path, destination: Path) -> None:
    if destination.exists() and any(destination.iterdir()):
        raise PublicationError("destination is non-empty")
    if destination.exists():
        destination.rmdir()
    destination.parent.mkdir(parents=True,exist_ok=True)
    os.replace(staging,destination)

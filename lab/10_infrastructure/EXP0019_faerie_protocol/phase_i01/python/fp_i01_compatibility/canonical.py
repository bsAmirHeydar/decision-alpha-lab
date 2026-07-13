"""Canonical serialization and hashing for FP-I01 compatibility evidence."""
from __future__ import annotations
from dataclasses import asdict, is_dataclass
from enum import Enum
from hashlib import sha256
from pathlib import Path
from typing import Any, Iterable
import json, math

class CanonicalizationError(ValueError): pass

def canonical_value(value: Any) -> Any:
    if is_dataclass(value): return canonical_value(asdict(value))
    if isinstance(value, Enum): return value.value
    if isinstance(value, Path): return value.as_posix()
    if isinstance(value, dict): return {str(k): canonical_value(value[k]) for k in sorted(value,key=str)}
    if isinstance(value, (list,tuple)): return [canonical_value(v) for v in value]
    if isinstance(value, set): return sorted(canonical_value(v) for v in value)
    if isinstance(value,float):
        if not math.isfinite(value): raise CanonicalizationError('non-finite float')
        if value == 0.0: return 0.0
        return float(format(value,'.15g'))
    if value is None or isinstance(value,(str,int,bool)): return value
    raise CanonicalizationError(f'unsupported canonical type: {type(value)!r}')

def canonical_json(value: Any) -> str:
    return json.dumps(canonical_value(value),ensure_ascii=False,sort_keys=True,separators=(',',':'))

def canonical_sha256(value: Any) -> str:
    return sha256(canonical_json(value).encode('utf-8')).hexdigest()

def file_sha256(path: Path) -> str:
    h=sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def aggregate_files_hash(root: Path, paths: Iterable[Path]) -> str:
    material=[]
    for path in sorted(paths,key=lambda p:p.relative_to(root).as_posix()):
        material.append({'path':path.relative_to(root).as_posix(),'sha256':file_sha256(path),'size_bytes':path.stat().st_size})
    return canonical_sha256(material)

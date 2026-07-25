from __future__ import annotations
import hashlib, json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

def material(value: Any) -> Any:
    if is_dataclass(value): return material(asdict(value))
    if isinstance(value, Path): return value.resolve().as_posix()
    if isinstance(value, dict): return {str(k): material(v) for k,v in sorted(value.items(), key=lambda x:str(x[0]))}
    if isinstance(value, (list,tuple)): return [material(v) for v in value]
    return value

def canonical_json(value: Any) -> str: return json.dumps(material(value), sort_keys=True, separators=(",",":"), ensure_ascii=False)
def sha256_material(value: Any) -> str: return hashlib.sha256(canonical_json(value).encode()).hexdigest()
def sha256_file(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def write_json(path: Path, value: Any): path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(material(value),sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding='utf-8',newline='\n')
def write_jsonl(path: Path, rows): path.parent.mkdir(parents=True,exist_ok=True); path.write_text(''.join(canonical_json(x)+'\n' for x in rows),encoding='utf-8',newline='\n')

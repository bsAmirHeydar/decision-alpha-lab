from __future__ import annotations
import hashlib, json, re
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
SCHEMA_ROOT = REPO_ROOT / "registry" / "acl_os" / "schemas" / "v1"
TEMPLATE_ROOT = REPO_ROOT / "lab" / "11_strategy_factory" / "contexts" / "_template"
PLACEHOLDER_RE = re.compile(r"\b(?:REPLACE_ME(?:_[A-Z0-9_]+)?|TBD|TODO)\b")

def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def dump_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def result(passed: bool, code: str, message: str, **details: Any) -> dict[str,Any]:
    return {"passed":passed,"code":code,"message":message,"details":details}

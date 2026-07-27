from __future__ import annotations
from tools.repository_paths import RepositoryPaths, find_repository_root
import hashlib, json, re
from pathlib import Path
from typing import Any

REPO_ROOT = find_repository_root(__file__)
PATHS = RepositoryPaths.from_root(REPO_ROOT)
SCHEMA_ROOT = PATHS.acl_registry_root / "acl_02" / "schemas" / "v1"
TEMPLATE_ROOT = PATHS.authored_strategy_factory_context_root / "_template"
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

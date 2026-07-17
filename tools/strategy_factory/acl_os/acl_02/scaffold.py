from __future__ import annotations
import re,shutil
from pathlib import Path
from ..common import REPO_ROOT
_TEMPLATE=REPO_ROOT/"lab"/"11_strategy_factory"/"contexts"/"_acl_02_template"
_RE=re.compile(r"^CTX_[A-Z0-9_]{3,96}$")
def scaffold(context_id:str,destination:Path|None=None)->Path:
    if not _RE.fullmatch(context_id):raise ValueError("context_id must match ^CTX_[A-Z0-9_]{3,96}$")
    target=destination or REPO_ROOT/"lab"/"11_strategy_factory"/"contexts"/context_id
    if target.exists():raise FileExistsError(target)
    shutil.copytree(_TEMPLATE,target)
    for p in target.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".md",".yaml",".yml",".json",".txt"}:
            p.write_text(p.read_text(encoding="utf-8").replace("CTX_REPLACE_ME",context_id),encoding="utf-8")
    return target

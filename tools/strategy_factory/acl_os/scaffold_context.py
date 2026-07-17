from __future__ import annotations
import argparse, re, shutil
from pathlib import Path
from .common import REPO_ROOT, TEMPLATE_ROOT

CONTEXT_RE=re.compile(r"^CTX_[A-Z0-9_]{3,96}$")

def scaffold(context_id: str, destination: Path|None=None) -> Path:
    if not CONTEXT_RE.fullmatch(context_id):
        raise ValueError("context_id must match ^CTX_[A-Z0-9_]{3,96}$")
    root=destination or (REPO_ROOT/"lab"/"11_strategy_factory"/"contexts"/context_id)
    if root.exists(): raise FileExistsError(f"destination already exists: {root}")
    shutil.copytree(TEMPLATE_ROOT,root)
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".md",".yaml",".yml",".json",".txt"}:
            text=p.read_text(encoding="utf-8").replace("CTX_REPLACE_ME",context_id)
            p.write_text(text,encoding="utf-8")
    return root

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("context_id"); ap.add_argument("--destination",type=Path)
    ns=ap.parse_args()
    print(scaffold(ns.context_id,ns.destination))
    return 0
if __name__=="__main__": raise SystemExit(main())

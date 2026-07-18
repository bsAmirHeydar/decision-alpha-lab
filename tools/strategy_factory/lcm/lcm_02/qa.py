from __future__ import annotations
from pathlib import Path
from .static_validation import validate as static_validate
from .verify import verify_package

def run_qa(repo_root: Path, classification_root: Path):
    p=verify_package(classification_root); s=static_validate(repo_root)
    return {'passed':p['passed'] and s['passed'],'package':p,'static':s}

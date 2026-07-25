from __future__ import annotations
from pathlib import Path
from .static_validation import run as static_run
from .verify import verify_package

def run_qa(repo_root: Path, identity_root: Path):
    package=verify_package(identity_root);static=static_run(repo_root)
    return {'passed':package['passed'] and static['passed'],'package':package,'static':static}

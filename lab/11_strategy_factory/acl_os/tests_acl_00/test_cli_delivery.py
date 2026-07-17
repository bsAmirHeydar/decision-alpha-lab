from __future__ import annotations
import json,subprocess,sys
from pathlib import Path
from tools.strategy_factory.acl_os.common import REPO_ROOT
from tools.strategy_factory.acl_os.acl_00.validate_acl_00 import validate

FIX=REPO_ROOT/"lab"/"11_strategy_factory"/"acl_os"/"fixtures"/"acl_00"

def test_phase_validator_passes_after_metadata_exists():
    out=validate(REPO_ROOT); assert out["passed"],out

def test_cli_allows_valid_bundle(tmp_path:Path):
    p=subprocess.run([sys.executable,"-m","tools.strategy_factory.acl_os.acl_00.cli","evaluate",str(FIX/"valid_semantic_transition.json"),"--ledger",str(tmp_path/"audit.jsonl")],cwd=REPO_ROOT,text=True,capture_output=True); assert p.returncode==0,p.stderr; assert json.loads(p.stdout)["decision"]=="ALLOW"

def test_cli_denies_invalid_bundle():
    p=subprocess.run([sys.executable,"-m","tools.strategy_factory.acl_os.acl_00.cli","evaluate",str(FIX/"invalid_missing_approval.json")],cwd=REPO_ROOT,text=True,capture_output=True); assert p.returncode==2; assert json.loads(p.stdout)["decision"]=="DENY"

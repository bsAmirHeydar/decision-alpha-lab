from __future__ import annotations
import json,subprocess,sys
from jsonschema import Draft202012Validator
from tools.strategy_factory.acl_os.common import REPO_ROOT
from tools.strategy_factory.acl_os.acl_01.io import save_registry

def test_all_schemas_closed_and_valid():
    root=REPO_ROOT/"registry/acl_os/acl_01/schemas/v1"
    for p in root.glob("*.schema.json"):
        obj=json.loads(p.read_text()); Draft202012Validator.check_schema(obj); assert obj["additionalProperties"] is False

def test_policy_files_are_present():
    root=REPO_ROOT/"registry/acl_os/acl_01/policies/v1"; assert len(list(root.glob("*.yaml")))==15

def test_cli_validate(registry,tmp_path):
    p=tmp_path/"registry.json"; save_registry(p,registry)
    proc=subprocess.run([sys.executable,"-m","tools.strategy_factory.acl_os.acl_01.cli","--registry",str(p),"--repo-root",str(tmp_path),"validate"],cwd=REPO_ROOT,text=True,capture_output=True)
    assert proc.returncode==0,proc.stderr+proc.stdout

def test_mql5_boundary_static():
    root=REPO_ROOT/"lab/11_strategy_factory/mql5/Include/AlphaLab/ACL_OS/ACL01"
    text="\n".join(p.read_text() for p in root.glob("*.mqh"))
    assert "OrderSend(" not in text and "CTrade" not in text
    assert "ACL01_LIVE_ORDER_SUBMISSION_ALLOWED false" in text

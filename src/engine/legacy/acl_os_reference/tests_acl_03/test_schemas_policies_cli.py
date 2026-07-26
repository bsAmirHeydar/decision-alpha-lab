import json,subprocess,sys
from jsonschema import Draft202012Validator
import yaml
from src.engine.tooling.strategy_factory.acl_os.acl_03.policies import SCHEMA_ROOT,POLICY_ROOT
from src.engine.tooling.strategy_factory.acl_os.common import REPO_ROOT

def test_all_schemas_are_closed_and_valid():
    schemas=list(SCHEMA_ROOT.glob("*.schema.json"));assert len(schemas)>=20
    for p in schemas:
        o=json.loads(p.read_text());Draft202012Validator.check_schema(o);assert o["additionalProperties"] is False

def test_all_policies_parse_and_are_versioned():
    ps=list(POLICY_ROOT.glob("*.yaml"));assert len(ps)>=13
    for p in ps:
        o=yaml.safe_load(p.read_text());assert isinstance(o,dict);assert o["version"]=="1.0.0"

def test_cli_help():
    p=subprocess.run([sys.executable,"-m","src.engine.tooling.strategy_factory.acl_os.acl_03.cli","--help"],cwd=REPO_ROOT,text=True,capture_output=True);assert p.returncode==0;assert "compile" in p.stdout

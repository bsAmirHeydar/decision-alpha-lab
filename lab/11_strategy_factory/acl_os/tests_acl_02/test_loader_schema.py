import json
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator
from tools.strategy_factory.acl_os.acl_02.loader import ContextPackageLoader
from tools.strategy_factory.acl_os.acl_02.schema_validation import validate_schemas
from tools.strategy_factory.acl_os.acl_02.policies import SCHEMA_ROOT

def test_loads_all_sections(valid_root):
 p=ContextPackageLoader(valid_root).load();assert len(p)>=17;assert p["manifest"]["context_id"]=="CTX_REFERENCE_ALPHA"
def test_schema_valid(valid_root):
 p=ContextPackageLoader(valid_root).load();paths=p.pop("_paths");assert validate_schemas(p,paths)==[]
@pytest.mark.parametrize("schema",list(SCHEMA_ROOT.glob("*.schema.json")))
def test_all_schemas_are_metaschema_valid(schema):
 Draft202012Validator.check_schema(json.loads(schema.read_text()))
def test_path_escape_rejected(tmp_path,valid_root):
 import shutil,yaml
 shutil.copytree(valid_root,tmp_path/"ctx");p=tmp_path/"ctx/context_manifest.yaml";o=yaml.safe_load(p.read_text());o["contracts"]["scope"]="../../escape.yaml";p.write_text(yaml.safe_dump(o))
 with pytest.raises(Exception):ContextPackageLoader(tmp_path/"ctx").load()

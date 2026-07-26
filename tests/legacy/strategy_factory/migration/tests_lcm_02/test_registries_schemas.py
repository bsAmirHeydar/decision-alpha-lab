import json
from jsonschema import Draft202012Validator

def test_all_schemas_meta_valid(repo_root):
 for p in (repo_root/'registry/history/lcm/lcm_02/schemas/v1').glob('*.json'): Draft202012Validator.check_schema(json.loads(p.read_text()))
def test_all_policies_parse(repo_root):
 ps=list((repo_root/'registry/history/lcm/lcm_02/policies/v1').glob('*.json')); assert len(ps)>=20
 for p in ps: assert json.loads(p.read_text())['phase_id']=='LCM-02'
def test_closed_registries(repo_root):
 for p in (repo_root/'registry/history/lcm/lcm_02/registries/v1').glob('*.json'): assert json.loads(p.read_text())['closed']

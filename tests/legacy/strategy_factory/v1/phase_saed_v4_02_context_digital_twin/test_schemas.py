import json
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator

def test_all_schemas_closed(root):
 files=sorted((root/'schemas/legacy/strategy_factory/saed_v4_02').glob('*.schema.json'));assert len(files)>=28
 for p in files:
  s=json.loads(p.read_text());Draft202012Validator.check_schema(s);assert s.get('additionalProperties') is False
@pytest.mark.parametrize('name',['context_twin_manifest','twin_state_snapshot','twin_authority_boundary','phase_handoff_v4_02_to_v4_03'])
def test_unknown_field_rejected(root,name):
 s=json.loads((root/f'schemas/legacy/strategy_factory/saed_v4_02/{name}.schema.json').read_text());assert s['additionalProperties'] is False

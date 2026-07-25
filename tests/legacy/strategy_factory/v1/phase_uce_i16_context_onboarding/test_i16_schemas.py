from tools.repository_paths import find_repository_root
import json
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator
ROOT=find_repository_root(__file__)
SCHEMAS=sorted((ROOT/'schemas/legacy/strategy_factory/v3').glob('onboarding_*.schema.json'))
@pytest.mark.parametrize('path',SCHEMAS,ids=lambda p:p.stem)
def test_i16_schema_is_closed_and_valid(path):
 data=json.loads(path.read_text())
 Draft202012Validator.check_schema(data)
 assert data['additionalProperties'] is False
 assert data['$id'].startswith('urn:alpha-lab:strategy-factory:onboarding_')
 assert data['required']==['schema_version','artifact_id']

def test_exactly_twenty_five_i16_schemas():assert len(SCHEMAS)==25

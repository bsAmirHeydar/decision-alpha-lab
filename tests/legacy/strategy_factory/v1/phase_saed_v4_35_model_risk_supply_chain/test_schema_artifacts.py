from tools.repository_paths import find_repository_root
import json
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator
ROOT=find_repository_root(__file__)
ART=ROOT/'releases/history/strategy_factory/artifacts/saed_v4_35';SCH=ROOT/'schemas/legacy/strategy_factory/saed_v4_35'
PAIRS=[]
for p in sorted(ART.glob('GOLDEN_*.JSON')):
    s=SCH/(p.stem.lower()+'.schema.json');PAIRS.append((p,s))
@pytest.mark.parametrize('artifact_path,schema_path',PAIRS,ids=lambda p:p.name)
def test_golden_schema_pair(artifact_path,schema_path):
    assert schema_path.is_file();data=json.loads(artifact_path.read_text());schema=json.loads(schema_path.read_text());Draft202012Validator(schema).validate(data)

def test_all_schemas_closed():
    for s in SCH.glob('*.schema.json'):
        text=s.read_text();assert '"additionalProperties": false' in text

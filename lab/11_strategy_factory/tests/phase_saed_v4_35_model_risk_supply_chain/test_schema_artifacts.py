import json
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[4]
ART=ROOT/'lab/11_strategy_factory/artifacts/saed_v4_35';SCH=ROOT/'lab/11_strategy_factory/schemas/saed_v4_35'
PAIRS=[]
for p in sorted(ART.glob('GOLDEN_*.JSON')):
    s=SCH/(p.stem.lower()+'.schema.json');PAIRS.append((p,s))
@pytest.mark.parametrize('artifact_path,schema_path',PAIRS,ids=lambda p:p.name)
def test_golden_schema_pair(artifact_path,schema_path):
    assert schema_path.is_file();data=json.loads(artifact_path.read_text());schema=json.loads(schema_path.read_text());Draft202012Validator(schema).validate(data)

def test_all_schemas_closed():
    for s in SCH.glob('*.schema.json'):
        text=s.read_text();assert '"additionalProperties": false' in text

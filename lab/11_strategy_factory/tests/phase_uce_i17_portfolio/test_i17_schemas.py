import json
from pathlib import Path
import jsonschema,pytest
ROOT=Path(__file__).resolve().parents[2]
SCHEMAS=ROOT/'schemas/v3'
FILES=sorted(SCHEMAS.glob('portfolio_*.schema.json'))
def test_all_i17_schemas_are_closed_and_parseable():
 assert len(FILES)>=25
 for p in FILES:
  s=json.loads(p.read_text());jsonschema.Draft202012Validator.check_schema(s);assert s['additionalProperties'] is False
@pytest.mark.parametrize('p',FILES)
def test_schema_accepts_minimum_artifact(p):
 s=json.loads(p.read_text());jsonschema.validate({'schema_version':'1.0.0','artifact_id':'x','artifact_hash':'a'*64},s)

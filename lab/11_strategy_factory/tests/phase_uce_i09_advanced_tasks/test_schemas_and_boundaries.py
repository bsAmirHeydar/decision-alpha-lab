from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
def test_i09_schemas_are_closed_json_objects():
 files=list((ROOT/'schemas/v3').glob('*advanced*.schema.json'))+list((ROOT/'schemas/v3').glob('*ranking*.schema.json'))+list((ROOT/'schemas/v3').glob('*policy*.schema.json'))+list((ROOT/'schemas/v3').glob('*survival*.schema.json'))+list((ROOT/'schemas/v3').glob('*quantile*.schema.json'))+list((ROOT/'schemas/v3').glob('*treatment*.schema.json'))
 assert files
 for f in files:
  o=json.loads(f.read_text());assert o.get('type')=='object';assert o.get('additionalProperties') is False

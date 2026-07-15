import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
def test_all_schemas_are_closed_and_valid_json():
 files=sorted((ROOT/'lab/11_strategy_factory/schemas/saed_v4_08').glob('*.schema.json'));assert len(files)>=27
 for p in files:
  x=json.loads(p.read_text());assert x.get('additionalProperties') is False;assert x['$schema'].endswith('2020-12/schema')

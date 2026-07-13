import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
def test_schema_count_and_closure():
 files=sorted((ROOT/'lab/11_strategy_factory/schemas/v3').glob('tournament_*.schema.json'));assert len(files)==25
 for p in files:
  d=json.loads(p.read_text());assert d['$schema'].endswith('2020-12/schema');assert d.get('additionalProperties') is False;assert d.get('type')=='object'

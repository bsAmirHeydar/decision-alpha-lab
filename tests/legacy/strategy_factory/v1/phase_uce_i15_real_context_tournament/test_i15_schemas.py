from tools.repository_paths import find_repository_root
import json
from pathlib import Path
ROOT=find_repository_root(__file__)
def test_schema_count_and_closure():
 files=sorted((ROOT/'schemas/legacy/strategy_factory/v3').glob('tournament_*.schema.json'));assert len(files)==25
 for p in files:
  d=json.loads(p.read_text());assert d['$schema'].endswith('2020-12/schema');assert d.get('additionalProperties') is False;assert d.get('type')=='object'

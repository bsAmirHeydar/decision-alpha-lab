import json
from pathlib import Path

def test_schema_catalog_closed():
 p=Path(__file__).resolve().parents[1]/'schemas'; files=list(p.glob('*.schema.json')); assert len(files)==15
 for f in files:
  d=json.loads(f.read_text()); assert d['additionalProperties'] is False and d['type']=='object' and d['$schema'].endswith('2020-12/schema')

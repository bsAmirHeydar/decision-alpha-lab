import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_closed_schemas_parse():
 files=list((ROOT/'schemas').glob('*.schema.json'));assert len(files)>=12
 for p in files:
  d=json.loads(p.read_text());assert d.get('$schema') and d.get('additionalProperties') is False

from pathlib import Path
import json
def test_all_schemas_closed():
 p=Path(__file__).resolve().parents[1]/'schemas';files=list(p.glob('*.json'));assert len(files)>=17
 for f in files:
  d=json.load(open(f));assert d.get('additionalProperties') is False

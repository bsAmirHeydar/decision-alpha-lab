import json
from pathlib import Path
def test_schemas_parse():
 p=Path(__file__).resolve().parents[1]/'schemas';files=list(p.glob('*.schema.json'));assert len(files)==15
 for f in files:assert json.loads(f.read_text())['$schema'].endswith('schema')

import json
from pathlib import Path
def test_schemas_are_closed():
    root=Path(__file__).resolve().parents[1]/'schemas';files=list(root.glob('*.json'));assert len(files)==18;assert all(json.loads(p.read_text()).get('additionalProperties') is False for p in files)

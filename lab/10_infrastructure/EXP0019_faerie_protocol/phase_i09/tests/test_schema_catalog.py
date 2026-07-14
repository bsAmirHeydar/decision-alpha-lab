import json
from pathlib import Path

def test_all_schemas_are_closed():
    root=Path(__file__).resolve().parents[1]/'schemas'
    files=list(root.glob('*.json'))
    assert len(files)==15
    for p in files:
        s=json.loads(p.read_text(encoding='utf-8'))
        assert s['type']=='object' and s['additionalProperties'] is False
        assert set(s['required'])==set(s['properties'])

def test_schema_ids_are_unique():
    root=Path(__file__).resolve().parents[1]/'schemas'
    ids=[json.loads(p.read_text(encoding='utf-8'))['$id'] for p in root.glob('*.json')]
    assert len(ids)==len(set(ids))

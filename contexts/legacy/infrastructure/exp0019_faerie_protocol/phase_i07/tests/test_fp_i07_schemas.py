import json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]/'schemas'
def test_schema_count(): assert len(list(BASE.glob('*.schema.json')))==15
def test_schemas_are_closed_objects():
    for p in BASE.glob('*.schema.json'):
        d=json.loads(p.read_text());assert d['type']=='object' and d.get('additionalProperties') is False and d.get('$schema')
def test_schema_titles_unique():
    titles=[json.loads(p.read_text())['title'] for p in BASE.glob('*.schema.json')];assert len(titles)==len(set(titles))

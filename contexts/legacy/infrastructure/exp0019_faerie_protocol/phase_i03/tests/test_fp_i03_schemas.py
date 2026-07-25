from tools.repository_paths import find_repository_root
import json
from pathlib import Path

ROOT=find_repository_root(__file__)
SCHEMA_ROOT=ROOT/'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i03/schemas'


def test_exact_public_schema_count():
    assert len(list(SCHEMA_ROOT.glob('*.schema.json')))==12


def test_all_public_schemas_are_closed_draft_2020_12():
    for path in SCHEMA_ROOT.glob('*.schema.json'):
        schema=json.loads(path.read_text())
        assert schema['$schema']=='https://json-schema.org/draft/2020-12/schema'
        assert schema['type']=='object'
        assert schema['additionalProperties'] is False
        assert set(schema['required'])<=set(schema['properties'])


def test_schema_ids_are_unique_and_versioned_by_phase():
    ids=[]
    for path in SCHEMA_ROOT.glob('*.schema.json'):
        schema=json.loads(path.read_text());ids.append(schema['$id'])
        assert '/fp-i03/' in schema['$id']
        assert schema['$id'].endswith(path.name)
    assert len(ids)==len(set(ids))

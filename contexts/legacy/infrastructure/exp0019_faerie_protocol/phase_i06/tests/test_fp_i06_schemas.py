from tools.repository_paths import find_repository_root
import json
from pathlib import Path
ROOT=find_repository_root(__file__)
def test_all_public_schemas_are_closed_and_versioned():
    schemas=sorted((ROOT/'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i06/schemas').glob('*.schema.json'))
    assert len(schemas)==15
    for path in schemas:
        schema=json.loads(path.read_text())
        assert schema['$schema']=='https://json-schema.org/draft/2020-12/schema'
        assert schema['type']=='object'
        assert schema['additionalProperties'] is False
        assert set(schema['required'])<=set(schema['properties'])
def test_hash_fields_are_sha256_constrained():
    for path in (ROOT/'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i06/schemas').glob('*.schema.json'):
        schema=json.loads(path.read_text())
        for name,definition in schema['properties'].items():
            if name.endswith('_hash') and definition.get('type')=='string':
                assert definition.get('pattern')=='^[0-9a-f]{64}$',(path.name,name)

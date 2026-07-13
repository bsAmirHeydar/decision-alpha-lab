import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
NAMES=(
'fp_i05_window_store_config','fp_i05_window_descriptor','fp_i05_symbol_window_aggregate','fp_i05_pair_window_aggregate',
'fp_i05_calendar_day_selection_item','fp_i05_calendar_day_selection','fp_i05_reference_level','fp_i05_reference_transition',
'fp_i05_reference_set','fp_i05_window_store_snapshot','fp_i05_revision_invalidation','fp_i05_window_store_checkpoint')

def test_all_public_schemas_exist_and_are_closed():
    base=ROOT/'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i05/schemas'
    for name in NAMES:
        schema=json.loads((base/f'{name}.schema.json').read_text())
        assert schema['$schema'].endswith('2020-12/schema')
        assert schema['type']=='object'
        assert schema['additionalProperties'] is False
        assert set(schema['required'])<=set(schema['properties'])

def test_hash_fields_use_sha256_pattern_when_direct_strings():
    base=ROOT/'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i05/schemas'
    for name in NAMES:
        schema=json.loads((base/f'{name}.schema.json').read_text())
        for field,definition in schema['properties'].items():
            if field.endswith('_hash') and definition.get('type')=='string':
                assert definition.get('pattern')=='^[0-9a-f]{64}$',(name,field)

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
I10_SCHEMAS = (
    'deep_algorithm_descriptor', 'view_tensor_spec', 'sequence_window_spec', 'sequence_artifact',
    'raster_spec', 'raster_artifact', 'pixel_audit_report', 'graph_spec', 'graph_artifact',
    'regime_novelty_prediction', 'fusion_prediction', 'deep_admission_evidence',
    'seed_run_observation', 'view_ablation_observation', 'export_assessment',
    'deep_qualification_report', 'distillation_report', 'quantization_report',
    'dependency_probe', 'adapter_plan', 'transfer_boundary', 'future_perturbation_audit',
    'deterministic_replay_audit', 'deep_registry_snapshot',
)


def test_i10_schema_catalog_is_closed_versioned_and_nontrivial():
    schema_root = ROOT / 'schemas' / 'v3'
    for name in I10_SCHEMAS:
        path = schema_root / f'{name}.schema.json'
        assert path.exists(), name
        schema = json.loads(path.read_text())
        assert schema['$schema'].endswith('2020-12/schema')
        assert schema['$id'].endswith(f'/{name}.schema.json')
        assert schema['type'] == 'object'
        assert schema['additionalProperties'] is False
        assert len(schema['required']) >= 3
        assert set(schema['required']) <= set(schema['properties'])


def test_i10_hash_fields_are_constrained_to_sha256_where_public():
    schema_root = ROOT / 'schemas' / 'v3'
    for name in ('sequence_artifact', 'raster_artifact', 'pixel_audit_report', 'graph_artifact', 'transfer_boundary'):
        schema = json.loads((schema_root / f'{name}.schema.json').read_text())
        for field, definition in schema['properties'].items():
            if field.endswith('_hash') and 'dataset_manifest_hash' not in field and definition.get('type') == 'string':
                assert definition.get('pattern') == '^[0-9a-f]{64}$', (name, field)

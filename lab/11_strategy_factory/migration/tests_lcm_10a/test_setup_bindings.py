from .conftest import j,jl
def test_all_setup_dependencies_accounted_without_treatment_identity():
 rows=jl('bindings/setup_treatment_binding_inventory.jsonl');assert len(rows)==60;assert len({x['setup_id'] for x in rows})==60;assert all(x['canonical_treatment_identity_id'] is None and not x['extraction_authorized'] and not x['execution_authorized'] for x in rows)

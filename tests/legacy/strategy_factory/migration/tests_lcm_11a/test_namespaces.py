import json
def test_namespace_contracts_are_unique_and_scoped(inventory_root,inventory):
    registry=json.loads((inventory_root/'visual_namespace_registry.json').read_text())
    contracts=registry['contracts']
    assert len(contracts)==len(inventory['objects'])
    ids=[x['namespace_id'] for x in contracts]
    templates=[x['canonical_object_id_template'] for x in contracts]
    assert len(ids)==len(set(ids))
    assert len(templates)==len(set(templates))
    assert all(x.startswith('ALV1::') for x in templates)
    assert all(x['deterministic'] and x['collision_resistant'] and x['randomness_forbidden'] for x in contracts)

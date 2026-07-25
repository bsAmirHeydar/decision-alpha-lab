import json
def test_lifecycle_contracts_own_cleanup(inventory_root,inventory):
    files=list((inventory_root/'visual_lifecycle_contracts').glob('*.json'))
    assert len(files)==len(inventory['objects'])
    for path in files:
        value=json.loads(path.read_text())
        assert len(value['canonical_states'])==6
        assert value['cleanup_scope'] in {'CANONICAL_INSTANCE_PREFIX_ONLY','OUTPUT_PATH_OWNED'}
        if value['validation_status']=='BLOCKED':assert value['blocker_ids']

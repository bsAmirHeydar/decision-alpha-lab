import json
def test_anchor_contracts_are_complete_and_unknowns_block(inventory_root,inventory):
    files=list((inventory_root/'visual_anchor_contracts').glob('*.json'))
    assert len(files)==len(inventory['objects'])
    for path in files:
        value=json.loads(path.read_text())
        assert value['anchor_kind']
        assert value['availability_time_semantics']
        if value['validation_status']=='BLOCKED':assert value['blocker_ids']

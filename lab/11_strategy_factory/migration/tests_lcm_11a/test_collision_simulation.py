import json
def test_canonical_collision_simulation_is_zero(inventory_root):
    report=json.loads((inventory_root/'multi_instance_collision_report.json').read_text())
    assert report['canonical_collision_count']==0
    assert report['canonical_simulation']['result']=='PASS'
    assert report['canonical_simulation']['scenario_count']>0

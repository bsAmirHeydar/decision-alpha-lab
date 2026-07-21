from tools.strategy_factory.lcm.lcm_12b.io import load_json
def test_relocated_targets_are_not_orphans(reconciliation_root):
    report=load_json(reconciliation_root/"obsidian_orphan_report.json")
    assert report["relocated_target_orphan_count"]==0
    assert len(report["navigation_entry_points"])>=3

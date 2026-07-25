def test_acceptance_is_pass(load):
    report=load("reports/acceptance_report.json")
    assert report["passed"] is True
    assert all(report["gates"].values())
def test_no_move_or_delete(load):
    mapping=load("documentation_canonical_map.json")
    assert mapping["move_count"]==0
    assert mapping["delete_count"]==0

from tools.strategy_factory.lcm.lcm_12b.io import load_json
def test_hostile_review_attempted_required_failures(reconciliation_root):
    report=load_json(reconciliation_root/"reports/hostile_review_report.json")
    assert report["result"]=="PASS"
    assert all(value==0 for value in report["checks"].values())

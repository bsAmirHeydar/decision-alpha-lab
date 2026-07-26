from src.engine.tooling.strategy_factory.lcm.lcm_12b.io import load_json
def test_acceptance_non_compensatory(reconciliation_root):
    report=load_json(reconciliation_root/"reports/acceptance_report.json")
    assert report["passed"] is True
    assert report["failed_gates"] == []
    assert all(report["gates"].values())

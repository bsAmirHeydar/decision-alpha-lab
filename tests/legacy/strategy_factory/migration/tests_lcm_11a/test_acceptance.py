import json
def test_acceptance_gates(inventory_root):
    report=json.loads((inventory_root/'reports/acceptance_report.json').read_text())
    assert report['passed'] is True
    assert report['validation_status']=='PASS'
    assert all(report['gates'].values())

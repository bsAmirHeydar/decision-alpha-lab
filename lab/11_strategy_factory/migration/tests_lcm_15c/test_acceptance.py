import json
def test_acceptance(package_root):d=json.loads((package_root/'reports/acceptance_report.json').read_text());assert d['report_result']=='PASS'

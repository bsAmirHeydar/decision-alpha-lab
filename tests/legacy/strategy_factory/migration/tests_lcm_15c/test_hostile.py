import json
def test_hostile(package_root):d=json.loads((package_root/'reports/hostile_review_report.json').read_text());assert d['report_result']=='PASS' and all(x['result']=='PASS' for x in d['checks'])

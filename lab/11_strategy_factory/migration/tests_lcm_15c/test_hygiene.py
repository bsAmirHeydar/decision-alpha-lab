import json
def test_hygiene(package_root):d=json.loads((package_root/'repository_hygiene_report.json').read_text());assert d['report_result']=='PASS_RESIDUALS_EXPLICIT'

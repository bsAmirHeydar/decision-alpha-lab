import json
from conftest import CLOSURE
def test_parity_closes_all_packages():
 r=json.loads((CLOSURE/'parity/execution_parity_report.json').read_text());assert r['package_count']==422;assert r['passed_count']==422;assert r['failed_count']==0;assert r['submission_attempt_count']==0

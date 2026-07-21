import json
from conftest import CLOSURE
def test_acceptance_gate():
 a=json.loads((CLOSURE/'reports/acceptance_report.json').read_text());assert a['acceptance_gate_passed'];assert all(a['gates'].values())

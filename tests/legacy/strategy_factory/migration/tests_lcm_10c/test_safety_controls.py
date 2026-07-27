import json
from .conftest import CLOSURE
def test_all_safety_controls_fail_closed():
 r=json.loads((CLOSURE/'safety/safety_control_test_report.json').read_text());assert r['failed_count']==0;assert r['passed_count']==r['case_count'];assert r['submission_attempt_count']==0
def test_required_controls_present():
 r=json.loads((CLOSURE/'safety/safety_control_test_report.json').read_text());codes={x['control_code'] for x in r['controls']};assert {'DUPLICATE_DECISION','STALE_QUOTE','EXCESSIVE_SPREAD','INVALID_TICK_ALIGNMENT','INVALID_VOLUME','INVALID_STOP_DISTANCE','CLOSED_SESSION','MISSING_QUOTE','RECONCILIATION_MISMATCH','KILL_SWITCH_ACTIVE'}<=codes

import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];out=json.loads((ROOT/'lab/11_strategy_factory/examples/saed_v4_38/reference_output.json').read_text());m=out['external_evidence_matrix'];c=out['certificate']
if m['actual_metaeditor_compile_passed'] or m['actual_terminal_parity_passed'] or m['external_runtime_evidence_complete']:raise SystemExit('external gate falsely passed')
if c['production_authorized'] or c['capital_activation_allowed'] or c['order_submission_allowed']:raise SystemExit('authority falsely granted')
print(json.dumps({'phase':'SAED_V4_38','metaeditor_compile':'pending_external','terminal_parity':'pending_external','production_authorized':False,'passed':True}))

from __future__ import annotations
from typing import Any
from .canonical import stable_id,with_digest
from .gate_registry import HARD_FAIL_GATES
from .policies import GATE_IDS

def decide(candidate:dict[str,Any],gates:dict[str,dict[str,Any]])->dict[str,Any]:
    if candidate['lane']=='DIAGNOSTIC': status='DIAGNOSTIC_EXCLUDED'; reasons=['DIAGNOSTIC_LANE_NON_SELECTABLE']
    elif candidate['origin']=='BASELINE': status='BASELINE_REFERENCE_ONLY'; reasons=['BASELINE_NOT_PROMOTABLE']
    elif any(gates[g]['status']=='FAIL' for g in HARD_FAIL_GATES): status='VALIDATION_FAILED'; reasons=['HARD_VALIDATION_GATE_FAILED']
    elif any(gates[g]['status'] in {'FAIL','UNKNOWN'} for g in GATE_IDS): status='EVIDENCE_INSUFFICIENT'; reasons=['ONE_OR_MORE_REQUIRED_GATES_NOT_PASSED']
    else: status='VALIDATION_ELIGIBLE_FOR_REPORTING'; reasons=['ALL_REFERENCE_GATES_PASSED']
    passed=sum(g['status']=='PASS' for g in gates.values()); failed=sum(g['status']=='FAIL' for g in gates.values()); unknown=sum(g['status']=='UNKNOWN' for g in gates.values()); na=sum(g['status']=='NOT_APPLICABLE' for g in gates.values())
    body={'schema_version':'1.0.0','decision_id':stable_id('VALDEC',candidate['setup_id'],candidate['candidate_result_digest']),'setup_id':candidate['setup_id'],'candidate_id':candidate['candidate_id'],'candidate_result_digest':candidate['candidate_result_digest'],'lane':candidate['lane'],'origin':candidate['origin'],'decision_status':status,'reason_codes':reasons,'gate_summary':{'passed':passed,'failed':failed,'unknown':unknown,'not_applicable':na,'total':len(gates)},'gate_result_digests':{k:gates[k]['gate_result_digest'] for k in sorted(gates)},'alpha_claim_allowed':False,'promotion_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False}
    return with_digest(body,'decision_digest')

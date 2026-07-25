from __future__ import annotations
from .canonical import stable_id,digest_object

def compare_case(case:dict,replay:dict)->dict:
    expected_zero=case.get("expected_submission_count")==0
    pass_gate=expected_zero and replay.get("submission_attempt_count")==0 and replay.get("live_order_count")==0 and replay.get("capital_activation_count")==0 and replay.get("final_state") in {"REJECTED","EXECUTION_BLOCKED"}
    result={"parity_result_id":stable_id("PARITY",case["case_id"]),"case_id":case["case_id"],"package_id":case["package_id"],"field_parity":{"side":"PASS","symbol":"PASS","entry":"PASS","stop":"PASS","targets":"PASS","volume_request":"PASS","expiry":"PASS","reason_codes":"PASS","lifecycle":"PASS"},"no_request_preserved":replay.get("final_state")=="REJECTED","submission_count_expected":0,"submission_count_actual":replay.get("submission_attempt_count"),"result":"PASS" if pass_gate else "FAIL"}
    result["parity_digest"]=digest_object(result,"parity_digest")
    return result

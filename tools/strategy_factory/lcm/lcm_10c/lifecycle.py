from __future__ import annotations
from .canonical import stable_id,digest_object
from .constants import CLAIM_CEILING,PRODUCER,TIME_SEMANTICS,OWNER,REVIEWER
from .safety import SafetyControlEngine
class DryRunLifecycleSimulator:
    def __init__(self):self.safety=SafetyControlEngine()
    def replay(self,case:dict,seen_decisions=())->dict:
        intent=case["intent"];events=[{"sequence":0,"state":"CREATED","reason":"REQUEST_RECEIVED"},{"sequence":1,"state":"VALIDATING","reason":"FAIL_CLOSED_VALIDATION"}]
        findings=self.safety.evaluate(intent,case.get("symbol_fixture") or {},seen_decisions)
        if findings:
            final="REJECTED";events.append({"sequence":2,"state":final,"reason_codes":[str(x.code) for x in findings]})
        else:
            final="DRY_RUN_ACCEPTED";events.append({"sequence":2,"state":final,"reason":"VALIDATED_NO_SUBMISSION"});events.append({"sequence":3,"state":"EXECUTION_BLOCKED","reason":"SUBMISSION_CAPABILITY_FALSE"});final="EXECUTION_BLOCKED"
        result={"schema_version":"1.0.0","producer":PRODUCER,"source_digests":[case["case_digest"]],"generated_at":None,"generated_time_semantics":TIME_SEMANTICS,"deterministic_identity":True,"owner":OWNER,"reviewer":REVIEWER,"claim_ceiling":CLAIM_CEILING,"validation_status":"PASS","replay_id":stable_id("DRYREPLAY",case["case_id"]),"case_id":case["case_id"],"package_id":case["package_id"],"events":events,"findings":[x.to_dict() for x in findings],"final_state":final,"submission_attempt_count":0,"live_order_count":0,"paper_order_count":0,"capital_activation_count":0}
        result["replay_digest"]=digest_object(result,"replay_digest")
        return result

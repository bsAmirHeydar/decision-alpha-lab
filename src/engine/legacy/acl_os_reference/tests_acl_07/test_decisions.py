from src.engine.tooling.strategy_factory.acl_os.acl_07.decision_engine import decide
from src.engine.tooling.strategy_factory.acl_os.acl_07.gate_engine import result
from src.engine.tooling.strategy_factory.acl_os.acl_07.policies import GATE_IDS

def gates(status='PASS'): return {g:result(g,status,[],{},[]) for g in GATE_IDS}
def candidate(lane='RESEARCH',origin='AI'): return {'setup_id':'S','candidate_id':'C','candidate_result_digest':'sha256:'+'0'*64,'lane':lane,'origin':origin}
def test_diagnostic_excluded(): assert decide(candidate('DIAGNOSTIC','BASELINE'),gates())['decision_status']=='DIAGNOSTIC_EXCLUDED'
def test_baseline_reference_only(): assert decide(candidate('RESEARCH','BASELINE'),gates())['decision_status']=='BASELINE_REFERENCE_ONLY'
def test_unknown_is_insufficient():
 g=gates(); g['EXECUTION_ECONOMICS']=result('EXECUTION_ECONOMICS','UNKNOWN',[],{},[]); assert decide(candidate(),g)['decision_status']=='EVIDENCE_INSUFFICIENT'
def test_hard_fail_is_failed():
 g=gates(); g['INPUT_INTEGRITY']=result('INPUT_INTEGRITY','FAIL',[],{},[]); assert decide(candidate(),g)['decision_status']=='VALIDATION_FAILED'
def test_all_pass_is_reporting_eligible(): assert decide(candidate(),gates())['decision_status']=='VALIDATION_ELIGIBLE_FOR_REPORTING'
def test_decision_never_promotes(): assert decide(candidate(),gates())['promotion_allowed'] is False

from saed_v4_robust_optimization_regret.certificates import verify_certificate
from saed_v4_robust_optimization_regret.service import run_reference

def test_certificate_valid(result):assert verify_certificate(result['certificate'])
def test_certificate_authorities_false(result):
 c=result['certificate'];assert all(not c[k] for k in ['runtime_executable','decision_authority','risk_allocation_authority','promotion_authority','execution_authority','production_authority'])
def test_replay(config,upstream,score,result):assert run_reference(config,upstream,score)['reference_run_hash']==result['reference_run_hash']
def test_handoff(result):
 h=result['handoff'];assert h['next_phase']=='SAED_V4_22' and all(h['entry_gates'].values()) and not any(h['authority'].values())
def test_claim_ceiling(result):
 c=result['claim_tier_report'];assert c['robust_optimization_implemented'] and not c['real_policy_value_established'] and not c['production_authorization']

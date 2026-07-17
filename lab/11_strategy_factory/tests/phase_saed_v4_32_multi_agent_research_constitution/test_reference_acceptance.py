def test_certificate_accepts_reference(result):
 assert result["certificate"]["accepted_reference"]
 assert result["certificate"]["all_gates_passed"]
def test_handoff_targets_v433(result): assert result["handoff"]["next_phase"]=="SAED_V4_33"
def test_authority_zero(result): assert all(v is False for v in result["authority"]["authority"].values())
def test_replay_exact(result): assert result["replay"]["deterministic"] and result["reproduction"]["exact_match"]
def test_no_external_runtime_claim(result): assert result["certificate"]["external_agent_runtime_claim"] is False

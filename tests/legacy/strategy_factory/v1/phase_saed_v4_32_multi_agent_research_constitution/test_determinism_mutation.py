import copy,pytest
from saed_v4_multi_agent_research_constitution.service import run
from saed_v4_multi_agent_research_constitution.canonical import content_hash
from saed_v4_multi_agent_research_constitution.errors import SAEDV432Error

def test_exact_determinism(inputs): assert content_hash(run(inputs))==content_hash(run(inputs))
@pytest.mark.parametrize("cap",["promotion","runtime_activation","risk_allocation","order_submission","credential_access","production_release","online_learning","context_truth_mutation","evidence_role_mutation","counterexample_suppression","residual_risk_waiver"])
def test_granting_forbidden_capability_is_detected(inputs,cap):
 x=copy.deepcopy(inputs); row=next(c for c in x["capabilities"] if c["capability_id"]==cap); row["allowed_roles"]=["orchestrator"]; row["denied_in_phase"]=False
 with pytest.raises(SAEDV432Error): run(x)
@pytest.mark.parametrize("role",["orchestrator","hypothesis","data_audit","leakage_sentinel","statistical_adversary","model_engineering","causal_auditor","execution_auditor","evidence_curator"])
def test_nonhuman_approval_authority_rejected(inputs,role):
 x=copy.deepcopy(inputs); row=next(r for r in x["roles"] if r["role_id"]==role); row["may_approve_research"]=True
 with pytest.raises(SAEDV432Error): run(x)

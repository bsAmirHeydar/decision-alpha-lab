import copy,pytest
from saed_v4_multi_agent_research_constitution.identities import freeze_roles,freeze_agents,memory_boundary
from saed_v4_multi_agent_research_constitution.authority import freeze_capabilities,authorize,authority_boundary
from saed_v4_multi_agent_research_constitution.errors import IdentityError,AuthorityError

def _built(inputs):
 r=freeze_roles(inputs["roles"]); a=freeze_agents(inputs["agents"],r); c=freeze_capabilities(inputs["capabilities"],r); return r,a,c

def test_memory_namespaces_unique(inputs):
 _,a,_=_built(inputs); b=memory_boundary(a); assert b["namespace_unique"] and b["cross_agent_write_denied"]
@pytest.mark.parametrize("forbidden",["promotion","runtime_activation","risk_allocation","order_submission","credential_access","production_release","online_learning","context_truth_mutation","evidence_role_mutation","counterexample_suppression","residual_risk_waiver"])
def test_forbidden_capability_denied_for_every_agent(inputs,forbidden):
 _,a,c=_built(inputs)
 for agent in a["agents"]: assert not authorize(agent,forbidden,c)["allowed"]
@pytest.mark.parametrize("unknown",["shell_root","edit_constitution","access_live_broker","delete_evidence","arbitrary_network"])
def test_unknown_capability_denied_by_default(inputs,unknown):
 _,a,c=_built(inputs); assert authorize(a["agents"][0],unknown,c)["reason"]=="deny_by_default"
@pytest.mark.parametrize("role,cap",[("hypothesis","propose_hypothesis"),("model_engineering","implement_model"),("statistical_adversary","challenge_statistics"),("data_audit","audit_data"),("causal_auditor","audit_causality"),("execution_auditor","audit_execution"),("evidence_curator","curate_evidence"),("orchestrator","schedule_task"),("human_reviewer","approve_research_checkpoint")])
def test_allowed_role_capability(inputs,role,cap):
 _,a,c=_built(inputs); agent=next(x for x in a["agents"] if x["role_id"]==role); assert authorize(agent,cap,c)["allowed"]
def test_protected_access_requires_checkpoint(inputs):
 _,a,c=_built(inputs); agent=next(x for x in a["agents"] if x["role_id"]=="evidence_curator"); assert not authorize(agent,"read_protected_evidence",c)["allowed"]
def test_protected_access_with_independent_review(inputs):
 _,a,c=_built(inputs); agent=next(x for x in a["agents"] if x["role_id"]=="evidence_curator"); assert authorize(agent,"read_protected_evidence",c,["CHK-1"],["human_reviewer","statistical_adversary"])["allowed"]
def test_namespace_collision_fails(inputs):
 r=freeze_roles(inputs["roles"]); x=copy.deepcopy(inputs["agents"]); x[1]["memory_namespace"]=x[0]["memory_namespace"]
 with pytest.raises(IdentityError): freeze_agents(x,r)

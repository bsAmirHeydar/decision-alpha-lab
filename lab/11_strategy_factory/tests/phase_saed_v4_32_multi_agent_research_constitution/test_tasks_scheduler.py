import copy,pytest
from saed_v4_multi_agent_research_constitution.identities import freeze_roles,freeze_agents
from saed_v4_multi_agent_research_constitution.authority import freeze_capabilities
from saed_v4_multi_agent_research_constitution.tasks import freeze_tasks,build_delegation_graph,issue_tokens,deterministic_plan
from saed_v4_multi_agent_research_constitution.errors import TaskError

def _built(inputs):
 r=freeze_roles(inputs["roles"]); a=freeze_agents(inputs["agents"],r); c=freeze_capabilities(inputs["capabilities"],r); t=freeze_tasks(inputs["tasks"],a); return a,c,t

def test_task_graph_acyclic(inputs):
 _,_,t=_built(inputs); assert t["acyclic"]
def test_schedule_deterministic(inputs):
 _,_,t=_built(inputs); assert deterministic_plan(t)==deterministic_plan(t)
def test_tokens_ephemeral_and_nonlive(inputs):
 a,c,t=_built(inputs); l=issue_tokens(t,a,c); assert l["ephemeral"] and l["live_authority_tokens"]==0
@pytest.mark.parametrize("idx",range(11))
def test_self_review_mutation_fails(inputs,idx):
 r=freeze_roles(inputs["roles"]); a=freeze_agents(inputs["agents"],r); x=copy.deepcopy(inputs["tasks"]); x[idx]["reviewer_agent_ids"].append(x[idx]["owner_agent_id"])
 with pytest.raises(TaskError): freeze_tasks(x,a)
def test_cycle_fails(inputs):
 r=freeze_roles(inputs["roles"]); a=freeze_agents(inputs["agents"],r); x=copy.deepcopy(inputs["tasks"]); x[0]["depends_on"]=[x[-1]["task_id"]]
 with pytest.raises(TaskError): freeze_tasks(x,a)
@pytest.mark.parametrize("cap",["promotion","runtime_activation","risk_allocation","order_submission","production_release"])
def test_forbidden_task_capability_fails(inputs,cap):
 r=freeze_roles(inputs["roles"]); a=freeze_agents(inputs["agents"],r); c=freeze_capabilities(inputs["capabilities"],r); x=copy.deepcopy(inputs["tasks"]); x[0]["required_capabilities"]=[cap]; t=freeze_tasks(x,a)
 with pytest.raises(TaskError): build_delegation_graph(t,a,c)

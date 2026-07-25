import copy,pytest
from saed_v4_multi_agent_research_constitution.identities import freeze_roles,freeze_agents
from saed_v4_multi_agent_research_constitution.tasks import freeze_tasks
from saed_v4_multi_agent_research_constitution.provenance import freeze_sources
from saed_v4_multi_agent_research_constitution.claims import build_claim_graph
from saed_v4_multi_agent_research_constitution.adversary import run_challenges
from saed_v4_multi_agent_research_constitution.reviews import freeze_checkpoints,quorum_ledger
from saed_v4_multi_agent_research_constitution.incidents import build_incident_ledger
from saed_v4_multi_agent_research_constitution.errors import ReviewError,IncidentError

def _built(inputs):
 r=freeze_roles(inputs["roles"]); a=freeze_agents(inputs["agents"],r); t=freeze_tasks(inputs["tasks"],a); s=freeze_sources(inputs["sources"]); g=build_claim_graph(inputs["claims"],a,s); return a,t,g

def test_adversary_has_blocking_findings(inputs):
 a,t,g=_built(inputs); report,issues=run_challenges(inputs["challenges"],a,g); assert report["blocking_count"]==issues["open_count"] and issues["suppressed_count"]==0
def test_human_review_and_quorum(inputs):
 a,t,g=_built(inputs); c=freeze_checkpoints(inputs["checkpoints"],a); q=quorum_ledger(c,a); assert c["human_review_present"] and q["all_quorums_met"]
@pytest.mark.parametrize("idx",range(6))
def test_checkpoint_self_approval_fails(inputs,idx):
 a,t,g=_built(inputs); x=copy.deepcopy(inputs["checkpoints"]); x[idx]["reviewer_ids"].append(x[idx]["requester_agent_id"])
 with pytest.raises(ReviewError): freeze_checkpoints(x,a)
@pytest.mark.parametrize("idx",range(9))
def test_incident_counterexample_suppression_fails(inputs,idx):
 a,t,g=_built(inputs); x=copy.deepcopy(inputs["incidents"]); x[idx]["counterexamples_preserved"]=False
 with pytest.raises(IncidentError): build_incident_ledger(x,a,t)
def test_incident_ledger_contains_all_control_mutations(inputs):
 a,t,g=_built(inputs); x=build_incident_ledger(inputs["incidents"],a,t); assert x["incident_count"]==9 and x["automatic_containment"]

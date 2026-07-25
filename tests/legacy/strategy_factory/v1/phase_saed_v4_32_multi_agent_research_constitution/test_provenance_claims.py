import copy,pytest
from saed_v4_multi_agent_research_constitution.identities import freeze_roles,freeze_agents
from saed_v4_multi_agent_research_constitution.tasks import freeze_tasks
from saed_v4_multi_agent_research_constitution.provenance import freeze_sources,build_exposure_ledger,prompt_task_output_ledger
from saed_v4_multi_agent_research_constitution.claims import build_claim_graph,attribution_matrix,contradiction_ledger
from saed_v4_multi_agent_research_constitution.errors import ProvenanceError

def _built(inputs):
 r=freeze_roles(inputs["roles"]); a=freeze_agents(inputs["agents"],r); t=freeze_tasks(inputs["tasks"],a); s=freeze_sources(inputs["sources"]); return a,t,s

def test_exposure_complete(inputs):
 a,t,s=_built(inputs); x=build_exposure_ledger(t,s,a); assert x["complete"] and x["future_suffix_exposures"]==0
def test_prompt_output_complete(inputs):
 a,t,s=_built(inputs); x=prompt_task_output_ledger(t,a); assert x["complete_prompt_accounting"] and x["network_access"] is False
def test_claim_attribution_complete(inputs):
 a,t,s=_built(inputs); g=build_claim_graph(inputs["claims"],a,s); m=attribution_matrix(g,s); assert m["all_claims_attributed"]
def test_dissent_preserved(inputs):
 a,t,s=_built(inputs); g=build_claim_graph(inputs["claims"],a,s); d=contradiction_ledger(g); assert d["contradiction_count"]>=1 and d["suppressed_count"]==0
@pytest.mark.parametrize("source_index",range(6))
def test_future_source_mutation_fails(inputs,source_index):
 a,t,s=_built(inputs); x=copy.deepcopy(inputs["claims"]); sid=inputs["sources"][source_index]["source_id"]; x[0]["supporting_source_ids"]=[sid]; x[0]["known_time_epoch"]=1
 with pytest.raises(ProvenanceError): build_claim_graph(x,a,s)
def test_claim_cycle_fails(inputs):
 a,t,s=_built(inputs); x=copy.deepcopy(inputs["claims"]); x[0]["depends_on_claim_ids"]=[x[-1]["claim_id"]]
 with pytest.raises(ProvenanceError): build_claim_graph(x,a,s)
def test_unauthorized_protected_exposure_fails(inputs):
 a,t,s=_built(inputs); x=copy.deepcopy(inputs["tasks"]); x[0]["input_hashes"]=["source:SRC-PROT-001"]
 tx=freeze_tasks(x,a)
 with pytest.raises(ProvenanceError): build_exposure_ledger(tx,s,a)

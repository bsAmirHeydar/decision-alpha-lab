import copy,pytest
from saed_v4_multi_agent_research_constitution.identities import freeze_roles,freeze_agents
from saed_v4_multi_agent_research_constitution.tasks import freeze_tasks
from saed_v4_multi_agent_research_constitution.budgets import freeze_budgets,account
from saed_v4_multi_agent_research_constitution.errors import BudgetError

def _built(inputs):
 r=freeze_roles(inputs["roles"]); a=freeze_agents(inputs["agents"],r); t=freeze_tasks(inputs["tasks"],a); b=freeze_budgets(inputs["budgets"]); return t,b

def test_reference_within_budget(inputs):
 t,b=_built(inputs); assert account(b,t)["all_within_budget"]
@pytest.mark.parametrize("field",["compute_units","tool_calls","source_reads","human_review_minutes","max_agent_steps"])
def test_budget_exhaustion_hard_stops(inputs,field):
 t,b=_built(inputs); x=copy.deepcopy(inputs["budgets"]); x[0][field]=0; bx=freeze_budgets(x)
 with pytest.raises(BudgetError): account(bx,t)
def test_protected_exposure_budget_hard_stops(inputs):
 t,b=_built(inputs); x=copy.deepcopy(inputs["budgets"]); target=next(v for v in x if v["budget_id"]=="BUD-009"); target["protected_exposures"]=0; bx=freeze_budgets(x)
 with pytest.raises(BudgetError): account(bx,t)

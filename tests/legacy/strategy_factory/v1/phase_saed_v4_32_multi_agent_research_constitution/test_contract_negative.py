import copy,pytest
from saed_v4_multi_agent_research_constitution.service import run
from saed_v4_multi_agent_research_constitution.errors import SAEDV432Error
@pytest.mark.parametrize("section",["constitution","roles","agents","capabilities","tasks","budgets","sources","claims","challenges","checkpoints","incidents"])
def test_unknown_field_rejected(inputs,section):
 x=copy.deepcopy(inputs); target=x[section];
 if isinstance(target,list): target[0]["unknown_field_v432"]=1
 else: target["unknown_field_v432"]=1
 with pytest.raises(SAEDV432Error): run(x)

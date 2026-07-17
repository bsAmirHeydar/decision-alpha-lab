import copy,pytest
from saed_v4_multi_agent_research_constitution.constitution import freeze_constitution
from saed_v4_multi_agent_research_constitution.errors import ConstitutionError,ContractError

def test_constitution_closed(inputs):
 c=freeze_constitution(inputs["constitution"]); assert c["closed_contract"] and len(c["clauses"])==13
@pytest.mark.parametrize("field,value",[("safe_default","allow"),("research_only",False),("phase","SAED_V4_31")])
def test_constitution_root_mutations_fail(inputs,field,value):
 x=copy.deepcopy(inputs["constitution"]); x[field]=value
 with pytest.raises((ConstitutionError,ContractError)): freeze_constitution(x)
@pytest.mark.parametrize("cid",["C-AUTH-001","C-AUTH-002","C-EVID-001","C-ID-001","C-TASK-001","C-PROV-001","C-REVIEW-001","C-BUDGET-001","C-MEM-001","C-SEC-001","C-SCI-001","C-INC-001","C-AMEND-001"])
def test_mandatory_clause_removal_fails(inputs,cid):
 x=copy.deepcopy(inputs["constitution"]); x["clauses"]=[c for c in x["clauses"] if c["clause_id"]!=cid]
 with pytest.raises(ConstitutionError): freeze_constitution(x)
@pytest.mark.parametrize("key,value",[("minimum_independent_approvals",1),("cooling_off_epochs",0),("retroactive_change_allowed",True),("self_approval_allowed",True)])
def test_unsafe_amendment_fails(inputs,key,value):
 x=copy.deepcopy(inputs["constitution"]); x["amendment_policy"][key]=value
 with pytest.raises((ConstitutionError,ContractError)): freeze_constitution(x)

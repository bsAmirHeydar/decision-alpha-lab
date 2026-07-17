import copy,pytest
from saed_v4_multi_agent_research_constitution.upstream import verify_upstream
from saed_v4_multi_agent_research_constitution.errors import UpstreamError,ContractError

def test_upstream_valid(inputs): assert verify_upstream(inputs["upstream_documents"])["entry_gate_passed"]
@pytest.mark.parametrize("idx,field,value",[(0,"document_hash","0"*64),(0,"document_id","bad"),(1,"document_hash","f"*64),(1,"document_id","bad"),(1,"phase","SAED_V4_30")])
def test_upstream_mutation_fails(inputs,idx,field,value):
 x=copy.deepcopy(inputs["upstream_documents"]); x[idx][field]=value
 with pytest.raises((UpstreamError,ContractError)): verify_upstream(x)
def test_upstream_document_missing_fails(inputs):
 with pytest.raises((UpstreamError,ContractError)): verify_upstream(inputs["upstream_documents"][:1])

import pytest
from saed_v4_graph_hypergraph_models.authority import assert_authority,AUTHORITY
from saed_v4_graph_hypergraph_models.errors import AuthorityError
def test_default_boundary():assert_authority({})
@pytest.mark.parametrize('key',[k for k,v in AUTHORITY.items() if not v])
def test_forbidden_authority(key):
 with pytest.raises(AuthorityError):assert_authority({key:True})

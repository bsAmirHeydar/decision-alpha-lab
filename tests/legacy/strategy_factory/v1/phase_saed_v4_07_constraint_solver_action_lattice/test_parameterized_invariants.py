import pytest
from .helpers import solve
@pytest.fixture(scope='module')
def output():return solve()
@pytest.mark.parametrize('index',range(38))
def test_each_node_has_no_execution_authority(output,index):
 n=output['action_lattice']['nodes'][index];assert not n['selection_authority'] and not n['execution_authority'];assert len(n['node_hash'])==64
@pytest.mark.parametrize('index',range(36))
def test_each_pruned_candidate_has_reason(output,index):
 r=output['solver_result']['pruning_ledger']['records'][index];assert r['failed_constraints'] and len(r['record_hash'])==64
@pytest.mark.parametrize('index',range(121))
def test_each_edge_is_auditable(output,index):
 e=output['action_lattice']['edges'][index];assert e['source_node_id']!=e['target_node_id'];assert e['semantic_claim']=='adjacency_only_not_preference';assert len(e['edge_hash'])==64

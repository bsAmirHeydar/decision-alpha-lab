import pytest
def test_no_cross_tenant_edges(output):assert output['dependencies']['cross_tenant_edges']==0 and output['impact']['cross_tenant_impact'] is False
@pytest.mark.parametrize('cell_idx',range(128))
def test_each_cell_has_dependency_edges(output,cell_idx):
 cid=f'CELL:CELL_{cell_idx+1:04d}';assert any(x['source']==cid or x['target']==cid for x in output['dependencies']['edges'])
def test_candidate_impact_complete(output):assert output['impact']['cell_ids']==['CELL_0127','CELL_0128'] and output['impact']['affected_node_count']>10

import pytest
@pytest.mark.parametrize('metric_idx',range(12))
def test_each_metric_has_full_cell_window_coverage(output,metric_idx):
 mid=output['policy']['metrics'][metric_idx]['metric_id'];rows=[x for x in output['ledger']['rows'] if x['metric_id']==mid];assert len(rows)==128*6
@pytest.mark.parametrize('cell_idx',range(128))
def test_each_cell_has_complete_surveillance(output,cell_idx):
 cid=f'CELL_{cell_idx+1:04d}';rows=[x for x in output['ledger']['rows'] if x['cell_id']==cid];assert len(rows)==12*6
@pytest.mark.parametrize('window_idx',range(6))
def test_each_window_has_complete_fleet_metric_coverage(output,window_idx):
 wid=f'W{window_idx+1:02d}';rows=[x for x in output['ledger']['rows'] if x['window_id']==wid];assert len(rows)==128*12
def test_ledger_complete(output):assert output['ledger']['coverage_complete'] is True and output['ledger']['coverage_bps']==10000
def test_no_future_suffix(output):assert output['ledger']['future_suffix_used'] is False and output['detection']['future_suffix_used'] is False

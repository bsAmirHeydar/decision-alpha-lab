import pytest
ACTIONS={'CONTINUE','WATCH','RESTRICT','QUARANTINE','RETIRE_CANDIDATE'}
@pytest.mark.parametrize('cell_idx',range(128))
def test_every_cell_has_one_deterministic_decision(output,cell_idx):
 cid=f'CELL_{cell_idx+1:04d}';rows=[x for x in output['fusion']['rows'] if x['cell_id']==cid];assert len(rows)==1;assert rows[0]['action'] in ACTIONS;assert len(rows[0]['decision_trace_hash'])==64
@pytest.mark.parametrize('cell_idx',range(116))
def test_normal_reference_cells_continue(output,cell_idx):
 cid=f'CELL_{cell_idx+1:04d}';row=next(x for x in output['fusion']['rows'] if x['cell_id']==cid);assert row['action']=='CONTINUE'
def test_degradation_ladder_present(output):
 c=output['fusion']['action_counts'];assert c['WATCH']>0 and c['RESTRICT']>0 and c['QUARANTINE']>0 and c['RETIRE_CANDIDATE']==2
def test_retirement_candidate_cells(output):assert [x['cell_id'] for x in output['fusion']['rows'] if x['action']=='RETIRE_CANDIDATE']==['CELL_0127','CELL_0128']

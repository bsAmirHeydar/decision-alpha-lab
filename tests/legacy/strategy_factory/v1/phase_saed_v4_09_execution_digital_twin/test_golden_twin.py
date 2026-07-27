from .helpers import built
from saed_v4_execution_twin.validation import validate_twin

def test_complete_cross_product_and_identity():
    cube,_,profile,twin=built();assert twin['twin_row_count']==len(cube['rows'])*len(profile.scenarios);assert twin['complete_exposure'];validate_twin(twin)

def test_source_rows_are_preserved():
    cube,_,profile,twin=built();expected={(r['row_id'],s.scenario_id) for r in cube['rows'] for s in profile.scenarios};observed={(r['source_row_id'],r['scenario_id']) for r in twin['rows']};assert expected==observed

def test_non_order_actions_never_fill():
    *_,twin=built();rows=[r for r in twin['rows'] if r['action_class'] in {'skip','abstain'}];assert rows and all(r['status']=='non_order' and r['fill_fraction']==0 for r in rows)

def test_incremental_costs_are_non_negative():
    *_,twin=built();assert all(r['incremental_execution_cost_points']>=0 and r['incremental_execution_cost_r']>=0 for r in twin['rows'])

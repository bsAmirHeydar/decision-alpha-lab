from tools.strategy_factory.lcm.lcm_04.io import read_json
from tools.strategy_factory.lcm.lcm_04.registries import CASE_TYPES

def test_closed_catalog(char_root):
    c=read_json(char_root/'cases/golden_case_catalog.json');assert c['closed'] and [x['case_type'] for x in c['cases']]==CASE_TYPES
def test_required_edge_cases_present():
    required={'RESTART','HISTORY_EXPANSION','MISSING_BAR','DST_TRANSITION','SESSION_BOUNDARY','TIMEFRAME_CHANGE','SYMBOL_CHANGE','MULTI_INSTANCE','DUPLICATE_TICK','CURRENT_BAR_INTRABAR','CLOSED_BAR_CONFIRMATION','DRAWING_LIFECYCLE','DRY_EXECUTION_REQUEST'}
    assert required.issubset(set(CASE_TYPES))

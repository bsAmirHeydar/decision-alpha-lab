from tools.repository_paths import find_repository_root
from pathlib import Path
import ast

REPO=find_repository_root(__file__)
MOD=REPO/'src/engine/tooling/strategy_factory/lcm/lcm_08b'

def test_adapter_has_no_order_or_drawing_api():
    text=(MOD/'legacy_adapter.py').read_text()
    forbidden=['OrderSend','CTrade','.Buy(','.Sell(','PositionOpen','PositionModify','PositionClose','ObjectCreate','ObjectSet','ChartRedraw']
    assert not [x for x in forbidden if x in text]

def test_python_modules_parse():
    for p in MOD.glob('*.py'):ast.parse(p.read_text(),filename=str(p))

def test_legacy_source_does_not_import_canonical_package():
    text=(REPO/'contexts/legacy/lab_experiments/EXP0015_intermarket_time_divergence/experiment.py').read_text()
    assert 'lcm_08b' not in text
    assert 'CTX_EXP0015_INTERMARKET_TIME_EXPERIMENT_3CD87586_V1' not in text

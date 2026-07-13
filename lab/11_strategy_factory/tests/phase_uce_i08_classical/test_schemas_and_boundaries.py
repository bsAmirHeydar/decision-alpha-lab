from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[4]
def test_i08_schemas_closed():
 names=('algorithm_descriptor','dependency_status','algorithm_registry_snapshot','calibration_record','explanation_request','feature_importance_record','explanation_artifact','benchmark_case','benchmark_observation','benchmark_report','classical_comparison_gate','algorithm_pack_manifest')
 for n in names:
  o=json.loads((ROOT/f'lab/11_strategy_factory/schemas/v3/{n}.schema.json').read_text());assert o.get('additionalProperties') is False
def test_no_live_authority():
 roots=[ROOT/'lab/11_strategy_factory/python/strategy_factory_classical_v3',ROOT/'mql5/Include/AlphaLab/StrategyFactory/ClassicalAlgorithms'];text='\n'.join(f.read_text(errors='ignore') for r in roots for f in r.rglob('*') if f.is_file());assert not re.search(r'\b(OrderSend|OrderCheck|PositionOpen|WebRequest)\s*\(',text)

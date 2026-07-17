from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
AR=ROOT/"lab/11_strategy_factory/artifacts/saed_v4_34"; SC=ROOT/"lab/11_strategy_factory/schemas/saed_v4_34"; EX=ROOT/"lab/11_strategy_factory/examples/saed_v4_34"; DOC=ROOT/"docs/strategy_factory_sovereign_context_intelligence_v4"; PY_ROOT=ROOT/"lab/11_strategy_factory/python"; MQL_INCLUDE=ROOT/"mql5/Include/StrategyFactory/SAED/V4_34"; MQL_EXPERT=ROOT/"mql5/Experts/StrategyFactory/SAED/V4_34"
if str(PY_ROOT) not in sys.path: sys.path.insert(0,str(PY_ROOT))
MAP=json.loads((Path(__file__).with_name("artifact_map.json")).read_text())
def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))

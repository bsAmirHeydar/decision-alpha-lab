from __future__ import annotations
from tools.repository_paths import find_repository_root
import json,sys
from pathlib import Path
ROOT=find_repository_root(__file__)
AR=ROOT/"releases/history/strategy_factory/artifacts/saed_v4_34"; SC=ROOT/"schemas/legacy/strategy_factory/saed_v4_34"; EX=ROOT/"examples/legacy/strategy_factory/saed_v4_34"; DOC=ROOT/"docs/strategy_factory_sovereign_context_intelligence_v4"; PY_ROOT=ROOT/"src/engine/packages"; MQL_INCLUDE=ROOT/"mql5/Include/StrategyFactory/SAED/V4_34"; MQL_EXPERT=ROOT/"mql5/Experts/StrategyFactory/SAED/V4_34"
if str(PY_ROOT) not in sys.path: sys.path.insert(0,str(PY_ROOT))
MAP=json.loads((Path(__file__).with_name("artifact_map.json")).read_text())
def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))

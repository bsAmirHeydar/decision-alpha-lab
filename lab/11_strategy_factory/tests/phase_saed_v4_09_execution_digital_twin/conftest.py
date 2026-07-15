from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[4]
PY=ROOT/'lab/11_strategy_factory/python'
if str(PY) not in sys.path: sys.path.insert(0,str(PY))

def load(rel): return json.loads((ROOT/rel).read_text(encoding='utf-8'))

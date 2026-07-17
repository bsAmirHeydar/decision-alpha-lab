from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/"lab/11_strategy_factory/python"))
FIXTURE=json.loads((ROOT/"lab/11_strategy_factory/examples/saed_v4_36/GOLDEN_INPUT.json").read_text())

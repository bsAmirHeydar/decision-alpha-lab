from __future__ import annotations
from tools.repository_paths import find_repository_root
import json,sys
from pathlib import Path
ROOT=find_repository_root(__file__)
sys.path.insert(0,str(ROOT/"src/engine/packages"))
FIXTURE=json.loads((ROOT/"examples/legacy/strategy_factory/saed_v4_36/GOLDEN_INPUT.json").read_text())

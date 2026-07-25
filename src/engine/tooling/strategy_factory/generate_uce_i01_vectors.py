#!/usr/bin/env python3
from __future__ import annotations
from tools.repository_paths import find_repository_root
import json,sys
from pathlib import Path
ROOT=find_repository_root(__file__)
sys.path.insert(0,str(ROOT/"src/engine/packages"))
from strategy_factory_contracts_v3.fixtures import build_cross_language_vectors
out=ROOT/"tests/fixtures/legacy/strategy_factory/v3/uce_i01_cross_language_vectors.json"
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(build_cross_language_vectors(),indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(out)

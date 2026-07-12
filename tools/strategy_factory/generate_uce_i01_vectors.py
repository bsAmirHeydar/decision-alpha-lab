#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"lab/11_strategy_factory/python"))
from strategy_factory_contracts_v3.fixtures import build_cross_language_vectors
out=ROOT/"lab/11_strategy_factory/test_vectors/v3/uce_i01_cross_language_vectors.json"
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(build_cross_language_vectors(),indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(out)

#!/usr/bin/env python3
"""Regenerate UCE-I11 deterministic conformance vectors."""
from __future__ import annotations
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PYROOT=ROOT/'lab'/'11_strategy_factory'/'python'
if str(PYROOT) not in sys.path: sys.path.insert(0,str(PYROOT))
from strategy_factory_experiments_v3.conformance import generate_vectors
OUT=ROOT/'lab'/'11_strategy_factory'/'test_vectors'/'v3'/'uce_i11_experiment_conformance_vectors.json'
OUT.write_text(json.dumps(generate_vectors(),indent=2,sort_keys=True)+'\n',encoding='utf-8')
print(OUT)

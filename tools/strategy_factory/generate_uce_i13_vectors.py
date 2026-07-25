#!/usr/bin/env python3
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
from strategy_factory_policy_v3.conformance import generate_vectors
p=ROOT/'lab/11_strategy_factory/test_vectors/v3/uce_i13_policy_conformance_vectors.json';p.write_text(json.dumps(generate_vectors(),indent=2,sort_keys=True)+'\n');print(p)

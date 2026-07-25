#!/usr/bin/env python3
from tools.repository_paths import find_repository_root
from pathlib import Path
import json,sys
ROOT=find_repository_root(__file__);sys.path.insert(0,str(ROOT/'src/engine/packages'))
from strategy_factory_policy_v3.conformance import generate_vectors
p=ROOT/'tests/fixtures/legacy/strategy_factory/v3/uce_i13_policy_conformance_vectors.json';p.write_text(json.dumps(generate_vectors(),indent=2,sort_keys=True)+'\n');print(p)

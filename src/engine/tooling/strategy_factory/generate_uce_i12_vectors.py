#!/usr/bin/env python3
from tools.repository_paths import find_repository_root
from pathlib import Path
import json,sys
ROOT=find_repository_root(__file__)
sys.path.insert(0,str(ROOT/'lab'/'11_strategy_factory'/'python'))
from strategy_factory_promotion_v3.canonical import canonical_value
from strategy_factory_promotion_v3.conformance import generate_vectors
path=ROOT/'lab'/'11_strategy_factory'/'test_vectors'/'v3'/'uce_i12_promotion_conformance_vectors.json'
path.parent.mkdir(parents=True,exist_ok=True)
path.write_text(json.dumps(canonical_value(generate_vectors()),indent=2,sort_keys=True)+'\n',encoding='utf-8')
print(path)

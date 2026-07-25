#!/usr/bin/env python3
from tools.repository_paths import find_repository_root
from pathlib import Path
import json
ROOT=find_repository_root(__file__)
base=ROOT/'releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/artifacts/uce_i19'
summary={'phase_id':'UCE-I19','artifact_count':len(list(base.glob('*.json'))),'activation_allowed':False,'artifacts':[p.name for p in sorted(base.glob('*.json'))]}
print(json.dumps(summary,indent=2))

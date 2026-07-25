from tools.repository_paths import find_repository_root
from pathlib import Path
import json,sys
ROOT=find_repository_root(__file__);sys.path.insert(0,str(ROOT/'src/engine/tooling/strategy_factory/saed_v4_16'))
from _schema_validator import validate
load=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
m=load('releases/history/strategy_factory/artifacts/saed_v4_16/CONTRACT_VALIDATION_MAP.JSON')
for row in m['contracts']:validate(load(row['document']),load(row['schema']))
print(f"SAED V4-16 closed-contract validation passed: {m['contract_count']} pairs")

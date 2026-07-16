from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(Path(__file__).parent))
from _schema_validator import validate
load=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
m=load('lab/11_strategy_factory/artifacts/saed_v4_17/CONTRACT_VALIDATION_MAP.JSON')
for row in m['contracts']:validate(load(row['document']),load(row['schema']))
print(f"SAED V4-17 closed-contract validation passed: {m['contract_count']} pairs")

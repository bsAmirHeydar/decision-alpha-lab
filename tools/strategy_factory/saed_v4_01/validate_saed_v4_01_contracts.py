#!/usr/bin/env python3
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
from saed_v4_data_foundation.contracts import load_document,validate_closed
S=ROOT/'lab/11_strategy_factory/schemas/saed_v4_01';E=ROOT/'lab/11_strategy_factory/examples/saed_v4_01';errors=[];count=0
for p in sorted(E.glob('*.json')):
 try:validate_closed(load_document(p),load_document(S/f'{p.stem}.schema.json'));count+=1
 except Exception as e:errors.append(f'{p.name}: {e}')
print(json.dumps({'status':'pass' if not errors else 'fail','validated':count,'errors':errors},indent=2));raise SystemExit(0 if not errors else 1)

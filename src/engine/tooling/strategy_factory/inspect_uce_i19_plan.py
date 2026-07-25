#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from strategy_factory_operations_v3.parsing import load_json_object

def main() -> int:
 p=argparse.ArgumentParser(); p.add_argument('plan',type=Path); a=p.parse_args(); value=load_json_object(a.plan)
 keys=('plan_id','source_commit','release_manifest_hash','environment_hash','target_hash','generation_hash','rollback_generation_hash','stage','authority_order','authority_broker','max_risk_units','starts_at_ms','expires_at_ms')
 print(json.dumps({k:value.get(k) for k in keys}|{'inspection_grants_authority':False},indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())

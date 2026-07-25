#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

REQUIRED_DIRS=('00_inputs','01_compile','02_startup','03_telemetry','04_reconciliation','05_incidents','06_eod','07_rollback','08_ramp','09_bundle')
REQUIRED_FILES=(
 '00_inputs/accepted_i18_release_manifest.json',
 '00_inputs/deployment_target.json',
 '00_inputs/deployment_plan.json',
 '00_inputs/operations_policy.json',
 '00_inputs/risk_envelope.json',
 '02_startup/startup_preflight.json',
 '03_telemetry/telemetry_window.json',
 '04_reconciliation/reconciliation_report.json',
 '06_eod/eod_report.json',
 '07_rollback/rollback_drill.json',
)
def sha(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def main() -> int:
 p=argparse.ArgumentParser(); p.add_argument('evidence_root',type=Path); p.add_argument('--output',type=Path); a=p.parse_args()
 root=a.evidence_root.resolve(); errors=[]; refs=[]
 for d in REQUIRED_DIRS:
  if not (root/d).is_dir(): errors.append('missing_dir:'+d)
 for rel in REQUIRED_FILES:
  path=root/rel
  if not path.is_file(): errors.append('missing_file:'+rel)
  else:
   try: json.loads(path.read_text(encoding='utf-8-sig'))
   except Exception as exc: errors.append(f'invalid_json:{rel}:{exc}')
   refs.append({'path':rel,'sha256':sha(path)})
 activation_allowed=False
 result={'phase_id':'UCE-I19','evidence_root':str(root),'status':'complete_structure_pending_human_review' if not errors else 'blocked','activation_allowed':activation_allowed,'errors':errors,'artifact_refs':refs,'note':'This structural evaluator never grants order or capital authority.'}
 text=json.dumps(result,indent=2,sort_keys=True)
 if a.output: a.output.write_text(text+'\n',encoding='utf-8')
 print(text); return 1 if errors else 0
if __name__=='__main__': raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

def sha(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def main() -> int:
 p=argparse.ArgumentParser(); p.add_argument('evidence_root',type=Path); p.add_argument('output',type=Path); a=p.parse_args()
 root=a.evidence_root.resolve(); refs=[]
 for path in sorted(root.rglob('*')):
  if path.is_file() and path.resolve()!=a.output.resolve(): refs.append({'path':path.relative_to(root).as_posix(),'sha256':sha(path),'size_bytes':path.stat().st_size})
 bundle={'phase_id':'UCE-I19','schema_version':'1.0.0','evidence_class':'external_unreviewed','activation_allowed':False,'maximum_stage':'frozen','maximum_risk_units':0.0,'blocking_reasons':['human_review_not_embedded','critical_gate_acceptance_not_embedded'],'artifact_refs':refs}
 a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(bundle,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(a.output); return 0
if __name__=='__main__': raise SystemExit(main())

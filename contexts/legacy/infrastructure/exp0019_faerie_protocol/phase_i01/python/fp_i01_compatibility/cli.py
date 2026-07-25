from __future__ import annotations
import argparse,json
from pathlib import Path
from .validator import validate

def main(argv=None):
 p=argparse.ArgumentParser();p.add_argument('repo',nargs='?',default='.');p.add_argument('--json',action='store_true');a=p.parse_args(argv)
 report,checks=validate(Path(a.repo).resolve());payload={'status':report.status.value,'report_hash':report.report_hash,'check_count':len(checks),'passed_count':sum(x['passed'] for x in checks),'failed':[x for x in checks if not x['passed']]}
 print(json.dumps(payload,indent=2,sort_keys=True) if a.json else f"FP-I01 {payload['status']}: {payload['passed_count']}/{payload['check_count']} checks; report={payload['report_hash']}")
 return 0 if not payload['failed'] else 1
if __name__=='__main__':raise SystemExit(main())

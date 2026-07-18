from __future__ import annotations
import argparse,json
from pathlib import Path
from .io import load_json
from .replay_validator import verify_generated_root
from .service import ACL07UnifiedValidationService

def main()->int:
    p=argparse.ArgumentParser(prog='acl07-validation'); sub=p.add_subparsers(dest='cmd',required=True)
    b=sub.add_parser('build'); b.add_argument('--acl06-root',type=Path,required=True); b.add_argument('--permit',type=Path,required=True); b.add_argument('--policy',type=Path,required=True); b.add_argument('--destination',type=Path,required=True); b.add_argument('--validated-at',required=True)
    v=sub.add_parser('verify'); v.add_argument('--root',type=Path,required=True)
    a=p.parse_args()
    if a.cmd=='build': out=ACL07UnifiedValidationService().validate(a.acl06_root,load_json(a.permit),load_json(a.policy),a.destination,a.validated_at)
    else: out=verify_generated_root(a.root)
    print(json.dumps(out,indent=2,sort_keys=True)); return 0 if out.get('passed',True) else 2
if __name__=='__main__': raise SystemExit(main())

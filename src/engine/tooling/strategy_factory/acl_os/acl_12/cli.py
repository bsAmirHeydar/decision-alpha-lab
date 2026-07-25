from __future__ import annotations
import argparse,json
from pathlib import Path
from .io import load_json
from .service import ACL12SecurityHardeningService
from .verify import verify_output
def main(argv=None)->int:
    p=argparse.ArgumentParser(prog='acl12-security-hardening'); sub=p.add_subparsers(dest='cmd',required=True)
    b=sub.add_parser('build'); b.add_argument('--acl11-root',type=Path,required=True); b.add_argument('--permit',type=Path,required=True); b.add_argument('--output',type=Path,required=True); b.add_argument('--hardened-at',default='2026-07-18T05:00:00Z')
    v=sub.add_parser('verify'); v.add_argument('--output',type=Path,required=True)
    a=p.parse_args(argv)
    if a.cmd=='build': result=ACL12SecurityHardeningService().build(a.acl11_root,load_json(a.permit),a.output,a.hardened_at)
    else: result=verify_output(a.output)
    print(json.dumps(result,indent=2,sort_keys=True)); return 0 if result.get('passed',True) else 1
if __name__=='__main__': raise SystemExit(main())

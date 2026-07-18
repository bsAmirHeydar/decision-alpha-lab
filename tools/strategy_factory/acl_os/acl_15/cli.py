from __future__ import annotations
import argparse,json
from pathlib import Path
from .io import load_json
from .service import ACL15FleetOperationsClosureService
from .verify import verify_output
from .qa import run as run_qa
def main(argv=None)->int:
    p=argparse.ArgumentParser(prog='acl15-fleet-operations-closure'); sub=p.add_subparsers(dest='cmd',required=True)
    b=sub.add_parser('build'); b.add_argument('--acl14-root',type=Path,required=True); b.add_argument('--permit',type=Path,required=True); b.add_argument('--policy',type=Path,required=True); b.add_argument('--output',type=Path,required=True); b.add_argument('--closed-at',default='2026-07-18T11:00:00Z')
    v=sub.add_parser('verify'); v.add_argument('--output',type=Path,required=True)
    q=sub.add_parser('qa'); q.add_argument('--root',type=Path,default=Path('.'))
    a=p.parse_args(argv)
    if a.cmd=='build': result=ACL15FleetOperationsClosureService().build(a.acl14_root,load_json(a.permit),load_json(a.policy),a.output,a.closed_at)
    elif a.cmd=='verify': result=verify_output(a.output)
    else: result=run_qa(a.root.resolve())
    print(json.dumps(result,indent=2,sort_keys=True)); return 0 if result.get('passed') else 1
if __name__=='__main__': raise SystemExit(main())

from __future__ import annotations
import argparse,json
from pathlib import Path
from .qa import run_qa
from .service import RunConfig,run_identity
from .verify import verify_installation,verify_package

def main(argv=None):
    p=argparse.ArgumentParser(prog='lcm-03');sub=p.add_subparsers(dest='cmd',required=True)
    b=sub.add_parser('run-identity');b.add_argument('--repo-root',type=Path,required=True);b.add_argument('--destination',type=Path,required=True);b.add_argument('--issued-at',default='2026-07-18T00:00:00Z')
    v=sub.add_parser('verify-package');v.add_argument('--identity-root',type=Path,required=True)
    i=sub.add_parser('verify-installation');i.add_argument('--repo-root',type=Path,required=True);i.add_argument('--identity-root',type=Path,required=True);i.add_argument('--patch-index',type=Path,required=True)
    q=sub.add_parser('qa');q.add_argument('--repo-root',type=Path,required=True);q.add_argument('--identity-root',type=Path,required=True)
    a=p.parse_args(argv)
    if a.cmd=='run-identity': result={'passed':True,'destination':str(run_identity(RunConfig(a.repo_root,a.destination,a.issued_at)))}
    elif a.cmd=='verify-package': result=verify_package(a.identity_root)
    elif a.cmd=='verify-installation': result=verify_installation(a.repo_root,a.identity_root,a.patch_index)
    else: result=run_qa(a.repo_root,a.identity_root)
    print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2));return 0 if result.get('passed',result.get('installation_passed',False)) else 1
if __name__=='__main__': raise SystemExit(main())

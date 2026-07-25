from __future__ import annotations
import argparse,json
from pathlib import Path
from .verify import verify_package,verify_installation
from .qa import run as run_qa

def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='cmd',required=True)
    a=s.add_parser('verify-package');a.add_argument('--pilot-root',type=Path,required=True)
    a=s.add_parser('verify-installation');a.add_argument('--repo-root',type=Path,required=True);a.add_argument('--pilot-root',type=Path,required=True);a.add_argument('--patch-index',type=Path,required=True)
    a=s.add_parser('qa');a.add_argument('--repo-root',type=Path,required=True);a.add_argument('--pilot-root',type=Path,required=True)
    args=p.parse_args()
    if args.cmd=='verify-package':out=verify_package(args.pilot_root)
    elif args.cmd=='verify-installation':out=verify_installation(args.repo_root,args.pilot_root,args.patch_index)
    else:out=run_qa(args.repo_root,args.pilot_root)
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()

from __future__ import annotations
import argparse, json
from pathlib import Path
from .io import load_json
from .qa import run_qa
from .replay_validator import verify_generated_root
from .service import ACL10PromotionStateService

def main() -> int:
    parser=argparse.ArgumentParser(prog='acl10'); sub=parser.add_subparsers(dest='cmd',required=True)
    build=sub.add_parser('build'); build.add_argument('--acl09-root',type=Path,required=True); build.add_argument('--permit',type=Path,required=True); build.add_argument('--promotion-policy',type=Path,required=True); build.add_argument('--destination',type=Path,required=True); build.add_argument('--evaluated-at',required=True)
    verify=sub.add_parser('verify'); verify.add_argument('root',type=Path)
    qa=sub.add_parser('qa'); qa.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[4])
    args=parser.parse_args()
    if args.cmd=='build': result=ACL10PromotionStateService().build(args.acl09_root,load_json(args.permit),load_json(args.promotion_policy),args.destination,args.evaluated_at)
    elif args.cmd=='verify': result=verify_generated_root(args.root)
    else: result=run_qa(args.repo_root)
    print(json.dumps(result,indent=2,sort_keys=True)); return 0 if result.get('passed',True) else 2
if __name__=='__main__': raise SystemExit(main())

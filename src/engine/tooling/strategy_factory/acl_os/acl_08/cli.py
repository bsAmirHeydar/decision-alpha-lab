from __future__ import annotations
from tools.repository_paths import find_repository_root
import argparse,json
from pathlib import Path
from .io import load_json
from .qa import run_qa
from .replay_validator import verify_generated_root
from .service import ACL08ReportingExperienceService
def main()->int:
    p=argparse.ArgumentParser(prog='acl08'); sub=p.add_subparsers(dest='cmd',required=True)
    b=sub.add_parser('build'); b.add_argument('--acl07-root',type=Path,required=True); b.add_argument('--permit',type=Path,required=True); b.add_argument('--policy',type=Path,required=True); b.add_argument('--destination',type=Path,required=True); b.add_argument('--reported-at',required=True); b.add_argument('--previous-root',type=Path)
    v=sub.add_parser('verify'); v.add_argument('root',type=Path)
    q=sub.add_parser('qa'); q.add_argument('--repo-root',type=Path,default=find_repository_root(__file__))
    a=p.parse_args()
    if a.cmd=='build': out=ACL08ReportingExperienceService().build(a.acl07_root,load_json(a.permit),load_json(a.policy),a.destination,a.reported_at,a.previous_root)
    elif a.cmd=='verify': out=verify_generated_root(a.root)
    else: out=run_qa(a.repo_root)
    print(json.dumps(out,indent=2,sort_keys=True)); return 0 if out.get('passed',True) else 2
if __name__=='__main__': raise SystemExit(main())

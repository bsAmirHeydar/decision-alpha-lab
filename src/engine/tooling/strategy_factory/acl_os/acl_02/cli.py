from __future__ import annotations
import argparse,json
from pathlib import Path
from .io import load_structured
from .service import ACL02ContextIntakeService
from .scaffold import scaffold
from .wizard import IntakeWizard

def main()->int:
    ap=argparse.ArgumentParser(prog="acl02"); sub=ap.add_subparsers(dest="cmd",required=True)
    s=sub.add_parser("scaffold");s.add_argument("context_id");s.add_argument("--destination",type=Path)
    v=sub.add_parser("evaluate");v.add_argument("context_root",type=Path);v.add_argument("--permit",type=Path);v.add_argument("--output-dir",type=Path)
    q=sub.add_parser("questions");q.add_argument("context_id");q.add_argument("--session-id",default="SESSION_LOCAL")
    ns=ap.parse_args()
    if ns.cmd=="scaffold":print(scaffold(ns.context_id,ns.destination));return 0
    if ns.cmd=="questions":print(json.dumps(IntakeWizard(ns.context_id,ns.session_id).next_questions(),indent=2));return 0
    permit=load_structured(ns.permit) if ns.permit else None
    out=ACL02ContextIntakeService().evaluate(ns.context_root,permit,ns.output_dir);print(json.dumps(out,indent=2,sort_keys=True));return 0 if out["readiness"]["blocking_count"]==0 else 2
if __name__=="__main__":raise SystemExit(main())

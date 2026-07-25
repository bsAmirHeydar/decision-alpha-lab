from __future__ import annotations
import argparse,json
from pathlib import Path
from .service import ACL03ContextCompilerService
from .io import load_json

def parser()->argparse.ArgumentParser:
    p=argparse.ArgumentParser(prog="alpha-acl03",description="Compile an approved ACL-02 Context package into deterministic ACL-03 IR")
    sub=p.add_subparsers(dest="command",required=True)
    c=sub.add_parser("compile");c.add_argument("context_root");c.add_argument("output_root");c.add_argument("--authority-permit",required=True);c.add_argument("--semantic-approval",required=True);c.add_argument("--acl02-readiness")
    return p

def main(argv=None)->int:
    a=parser().parse_args(argv)
    if a.command=="compile":
        result=ACL03ContextCompilerService().compile(Path(a.context_root),Path(a.output_root),load_json(Path(a.authority_permit)),load_json(Path(a.semantic_approval)),load_json(Path(a.acl02_readiness)) if a.acl02_readiness else None)
        print(json.dumps({"passed":result["passed"],"output_root":result["output_root"],"receipt_digest":result["receipt"]["receipt_digest"],"onboarding_decision":result["onboarding"]["decision"]},indent=2,sort_keys=True));return 0 if result["passed"] else 2
    return 2
if __name__=="__main__": raise SystemExit(main())

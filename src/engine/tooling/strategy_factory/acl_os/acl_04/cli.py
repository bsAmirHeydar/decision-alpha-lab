from __future__ import annotations
import argparse
import json
from pathlib import Path
from .service import ACL04DualSetupFactoryService
from .io import load_json, load_document


def parser() -> argparse.ArgumentParser:
    p=argparse.ArgumentParser(prog="alpha-acl04",description="Build a bounded canonical Setup universe from ACL-03 output")
    p.add_argument("compiled_root"); p.add_argument("output_root")
    p.add_argument("--authority-permit",required=True); p.add_argument("--search-authority",required=True); p.add_argument("--treatment-envelope",required=True)
    p.add_argument("--human-setup",action="append",default=[]); p.add_argument("--ai-request",action="append",default=[]); p.add_argument("--no-baselines",action="store_true")
    return p


def main(argv=None) -> int:
    a=parser().parse_args(argv)
    result=ACL04DualSetupFactoryService().build(compiled_root=Path(a.compiled_root),output_root=Path(a.output_root),authority_permit=load_json(Path(a.authority_permit)),search_authority=load_json(Path(a.search_authority)),treatment_envelope=load_json(Path(a.treatment_envelope)),human_setups=[load_document(Path(x)) for x in a.human_setup],ai_requests=[load_document(Path(x)) for x in a.ai_request],include_baselines=not a.no_baselines)
    print(json.dumps({"passed":result["passed"],"output_root":result["output_root"],"receipt_digest":result["receipt"]["receipt_digest"],"acl05_handoff_digest":result["handoff"]["handoff_digest"],"canonical_candidate_count":result["canonical_candidate_count"]},indent=2,sort_keys=True))
    return 0

if __name__=="__main__": raise SystemExit(main())

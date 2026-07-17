from __future__ import annotations
import argparse, json
from pathlib import Path
from .validate_context_package import validate_context
from .common import dump_json

def readiness(root: Path) -> dict:
    validation=validate_context(root,allow_placeholders=False)
    checks=validation.get("checks",[])
    by_code={}
    for c in checks: by_code.setdefault(c["code"],[]).append(c)
    package_ok=validation["passed"]
    stages={
      "semantic_validation":{"ready":package_ok,"missing":[c for c in checks if not c["passed"]]},
      "context_compile":{"ready":False,"missing":[{"code":"COMPILER_EVIDENCE_REQUIRED"}]},
      "research_entry":{"ready":False,"missing":[{"code":"DATA_AND_OCCURRENCE_SUPPORT_REQUIRED"}]},
      "statistical_eligibility":{"ready":False,"missing":[{"code":"IMMUTABLE_BATCH_AND_VALIDATION_REQUIRED"}]},
      "runtime_compatibility":{"ready":False,"missing":[{"code":"SIGNED_RUNTIME_AND_PARITY_REQUIRED"}]},
      "live_activation":{"ready":False,"missing":[{"code":"PROSPECTIVE_SECURITY_AND_CAPITAL_AUTHORIZATION_REQUIRED"}]}
    }
    return {"context_root":str(root),"overall_ready":False,"highest_possible_state":"SEMANTICALLY_VALIDATED" if package_ok else "DRAFT_CONTEXT","stages":stages,"claim_ceiling":"REFERENCE_ONLY"}

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("context_root",type=Path); ap.add_argument("--output",type=Path)
    ns=ap.parse_args(); out=readiness(ns.context_root)
    if ns.output: dump_json(ns.output,out)
    print(json.dumps(out,indent=2,sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())

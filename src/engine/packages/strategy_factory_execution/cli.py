from __future__ import annotations
import argparse, json
from pathlib import Path
from .models import PaperExecutionPolicy, ExecutionMode

def main() -> int:
    parser=argparse.ArgumentParser(description="Strategy Factory Phase 17 paper/shadow execution utilities")
    parser.add_argument("--validate-policy",type=Path)
    args=parser.parse_args()
    if args.validate_policy:
        raw=json.loads(args.validate_policy.read_text(encoding="utf-8"))
        raw["mode"]=ExecutionMode(raw["mode"])
        policy=PaperExecutionPolicy(**raw); policy.validate(); print(policy.derived_hash())
    return 0

if __name__ == "__main__": raise SystemExit(main())
